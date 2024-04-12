
import pyvips

# 打开原始图像
image = pyvips.Image.new_from_file("/home/xian/myfileserver/files/images/1.jpg")

# 生成瓦片图像
tiles_dir = "/home/xian/myfileserver/files/tiles/7"
image.dzsave(tiles_dir, suffix=".jpg", background=(0, 0, 0), tile_size=256, overlap=1, depth=3)


修改 Apache 的 htdocs 目录，您需要找到并修改 Apache 的配置文件。配置文件的路径会根据您的操作系统和安装方式而有所不同。

在大多数情况下，Apache 的配置文件名为 httpd.conf 或 apache2.conf，并位于以下路径之一：

Windows：C:\Program Files\Apache Group\ApacheX\conf\httpd.conf
macOS：/etc/apache2/httpd.conf
Linux：/etc/httpd/httpd.conf 或 /etc/apache2/apache2.conf
打开配置文件后，找到 DocumentRoot 的行，该行指定了 htdocs 目录的路径。默认情况下，该行应该类似于这样：

DocumentRoot "路径/到/htdocs"
将路径修改为您希望的新目录路径。例如，如果您要将 htdocs 目录改为 /var/www/mynewhtdocs，那么修改后的行将如下所示：

DocumentRoot "/var/www/mynewhtdocs"
完成修改后，保存配置文件并重启 Apache 服务器以使更改生效。

请注意，修改 Apache 的配置文件需要管理员或超级用户权限。在修改配置文件之前，建议先备份原始文件，以防止出现意外情况。
此外，修改 Apache 配置文件后，可能需要更新虚拟主机配置或重新配置其他相关设置，以确保服务器正常运行。