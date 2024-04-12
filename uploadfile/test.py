from deepzoom import DeepZoomGenerator

# 打开原始图像
original_image = "path/to/image.jpg"

# 创建Deep Zoom生成器
dzg = DeepZoomGenerator(original_image, tile_size=256, overlap=1, limit_bounds=False)

# 保存Deep Zoom图像
output_folder = "path/to/output_folder"
dzg.save(output_folder)