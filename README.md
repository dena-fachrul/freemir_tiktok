freemir TikTok Pre-Sales Calculation App | freemir TikTok 预售计算应用

A simple web application to calculate total SKU requirements from TikTok Shop "To Ship" reports, enriched with product names (English & Chinese) from the TAT database.

这是一个简单的网络应用程序，用于根据 TikTok Shop 的“待发货 (To Ship)”报告计算 SKU 总需求，并从 TAT 数据库中补充产品名称（英文和中文）。

📖 How to Use (For Users) | 如何使用（用户指南）

Open the App Link.
打开应用链接。

Upload the "TT To Ship" Excel File.
上传 "TT To Ship" Excel 文件。

Wait for the processing to finish.
等待处理完成。

Download the result in a clean Excel format.
下载整理好的 Excel 格式结果。

🚀 Setup Guide for GitHub & Streamlit Cloud | GitHub 和 Streamlit Cloud 设置指南

To run this app online and read the TAT.xlsx (Product Database) file, follow these steps:
要在线运行此应用程序并读取 TAT.xlsx（产品数据库）文件，请按照以下步骤操作：

Step 1: Prepare Files | 第一步：准备文件

Ensure you have these 3 files in a single folder on your computer:
确保您的电脑上的同一个文件夹中有以下 3 个文件：

streamlit_app.py (Main Python Code | 主 Python 代码)

requirements.txt (Library List | 依赖库列表)

TAT.xlsx (Your Product Database Excel | 您的产品数据库 Excel)

Step 2: Upload to GitHub | 第二步：上传至 GitHub

Create a new Repository on GitHub (e.g., freemir-sku-calc).
在 GitHub 上创建一个新的仓库（例如：freemir-sku-calc）。

Upload the three files above (streamlit_app.py, requirements.txt, and TAT.xlsx) together into the repository.
将上述三个文件（streamlit_app.py、requirements.txt 和 TAT.xlsx）一起上传到该仓库中。

IMPORTANT: The TAT.xlsx file must be in the root folder (outermost folder), alongside streamlit_app.py. Do not put it inside another folder.

重要提示： TAT.xlsx 文件必须位于根目录（最外层文件夹），与 streamlit_app.py 并列。请勿将其放入其他文件夹中。

Commit changes (Save).
提交更改（保存）。

Step 3: Deploy to Streamlit Cloud | 第三步：部署至 Streamlit Cloud

Go to share.streamlit.io.
访问 share.streamlit.io。

Login with GitHub.
使用 GitHub 登录。

Click "New App".
点击 "New App"（新建应用）。

Select the freemir-sku-calc repository you just created.
选择您刚刚创建的 freemir-sku-calc 仓库。

Ensure "Main file path" is streamlit_app.py.
确保 "Main file path"（主文件路径）为 streamlit_app.py。

Click Deploy.
点击 Deploy（部署）。

🔄 How to update TAT.xlsx? | 如何更新 TAT.xlsx？

If there are new products, simply update the TAT.xlsx file on your computer, then re-upload (replace) it to the same GitHub Repository. The app will automatically use the latest data after you refresh the web page.
如果有新产品，只需更新电脑上的 TAT.xlsx 文件，然后将其重新上传（替换）到同一个 GitHub 仓库。刷新网页后，应用程序将自动使用最新数据。
