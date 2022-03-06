import os
import io
import requests
import torch
import torchvision.transforms.functional as ttf
from PIL import ImageOps

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

steps = 250  # [25,50,100,150,250,500,1000]
width_height = [1280, 768]
clip_guidance_scale = 5000
tv_scale = 0 
range_scale = 150
sat_scale = 0 
cutn_batches = 4
skip_augs = False

# init settings
init_image = None 
init_scale = 1000
skip_steps = 0
perlin_mode = 'mixed'

# Get corrected sizes
side_x = (width_height[0] // 64) * 64
side_y = (width_height[1] // 64) * 64
if side_x != width_height[0] or side_y != width_height[1]:
    print(
        f"Changing output size to {side_x}x{side_y}. Dimensions must by multiples of 64."
    )

# # Update Model Settings
# timestep_respacing = f"ddim{steps}"
# diffusion_steps = (1000 // steps) * steps if steps < 1000 else steps
# model_config.update(
#     {
#         "timestep_respacing": timestep_respacing,
#         "diffusion_steps": diffusion_steps,
#     }
# )

def create_path(file_path):
    if not (os.path.exists(file_path)):
        try:
            original_umask = os.umask(0)
            os.makedirs(file_path, mode=0o777)
        finally:
            os.umask(original_umask)
        print(f"Made {file_path}")
    else:
        print(f"File path {file_path} exists.")


def fetch(url_or_path):
    if str(url_or_path).startswith("http://") or str(url_or_path).startswith(
        "https://"
    ):
        r = requests.get(url_or_path)
        r.raise_for_status()
        fd = io.BytesIO()
        fd.write(r.content)
        fd.seek(0)
        return fd
    return open(url_or_path, "rb")


def interp(t):
    return 3 * t**2 - 2 * t**3


def perlin(width, height, scale=10, device=None):
    gx, gy = torch.randn(2, width + 1, height + 1, 1, 1, device=device)
    xs = torch.linspace(0, 1, scale + 1)[:-1, None].to(device)
    ys = torch.linspace(0, 1, scale + 1)[None, :-1].to(device)
    wx = 1 - interp(xs)
    wy = 1 - interp(ys)
    dots = 0
    dots += wx * wy * (gx[:-1, :-1] * xs + gy[:-1, :-1] * ys)
    dots += (1 - wx) * wy * (-gx[1:, :-1] * (1 - xs) + gy[1:, :-1] * ys)
    dots += wx * (1 - wy) * (gx[:-1, 1:] * xs - gy[:-1, 1:] * (1 - ys))
    dots += (1 - wx) * (1 - wy) * (-gx[1:, 1:] * (1 - xs) - gy[1:, 1:] * (1 - ys))
    return dots.permute(0, 2, 1, 3).contiguous().view(width * scale, height * scale)


def perlin_ms(octaves, width, height, grayscale, device=device):
    out_array = [0.5] if grayscale else [0.5, 0.5, 0.5]
    for i in range(1 if grayscale else 3):
        scale = 2 ** len(octaves)
        oct_width = width
        oct_height = height
        for oct in octaves:
            p = perlin(oct_width, oct_height, scale, device)
            out_array[i] += p * oct
            scale //= 2
            oct_width *= 2
            oct_height *= 2
    return torch.cat(out_array)


def create_perlin_noise(octaves=[1, 1, 1, 1], width=2, height=2, grayscale=True):
    out = perlin_ms(octaves, width, height, grayscale)
    if grayscale:
        out = ttf.resize(size=(side_y, side_x), img=out.unsqueeze(0))
        out = ttf.to_pil_image(out.clamp(0, 1)).convert("RGB")
    else:
        out = out.reshape(-1, 3, out.shape[0] // 3, out.shape[1])
        out = ttf.resize(size=(side_y, side_x), img=out)
        out = ttf.to_pil_image(out.clamp(0, 1).squeeze())

    out = ImageOps.autocontrast(out)
    return out


def regen_perlin():
    if perlin_mode == "color":
        init = create_perlin_noise([1.5**-i * 0.5 for i in range(12)], 1, 1, False)
        init2 = create_perlin_noise([1.5**-i * 0.5 for i in range(8)], 4, 4, False)
    elif perlin_mode == "gray":
        init = create_perlin_noise([1.5**-i * 0.5 for i in range(12)], 1, 1, True)
        init2 = create_perlin_noise([1.5**-i * 0.5 for i in range(8)], 4, 4, True)
    else:
        init = create_perlin_noise([1.5**-i * 0.5 for i in range(12)], 1, 1, False)
        init2 = create_perlin_noise([1.5**-i * 0.5 for i in range(8)], 4, 4, True)

    init = (
        ttf.to_tensor(init)
        .add(ttf.to_tensor(init2))
        .div(2)
        .to(device)
        .unsqueeze(0)
        .mul(2)
        .sub(1)
    )
    del init2
    return init.expand(batch_size, -1, -1, -1)
