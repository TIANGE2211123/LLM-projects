import streamlit as st
from langchain.memory import ConversationBufferMemory
from chain import generate_response
from PIL import Image
import os
import base64


def start_page():

    # 显示背景图片
    image_path = 'pic.jpg'  # 确保路径正确
    st.image(image_path, use_column_width=True, caption='欢迎使用寻医问药小管家')
    col = st.columns([1,1,1,1,1])

    with col[2]:
        if st.button("开始使用"):
            st.session_state.page = "login"
            st.experimental_rerun()



def login_page():
    st.title('寻医问药小管家🩺')

    

  # 确保用户数据初始化
    if "users" not in st.session_state:
        st.session_state.users = {"default_user": "password123"}  # 示例用户数据
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.login_attempted = False  # 用于控制错误消息显示

    # 表单输入
    username = st.text_input("🙋🏻‍♂️ 用户名", placeholder="请输入用户名", key="username")
    password = st.text_input("🗝️ 密码", type="password", placeholder="请输入密码", key="password")

    # 自定义按钮样式
    button_style = """
    <style>
    .long-button {
        width: 100%;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
        margin-top: 10px;
    }
    .long-button:hover {
        background-color: #0056b3;
    }
    </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)

    # 创建一个包含一列的布局，用于登录按钮
    col = st.columns([1])

    with col[0]:
        # 登录按钮
        if st.markdown('<button class="long-button">登录</button>', unsafe_allow_html=True):
            st.session_state.login_attempted = True  # 设置登录尝试标记
            if username and password:
                if username in st.session_state.users and st.session_state.users[username] == password:
                    st.session_state.logged_in = True  # 设置登录状态
                    st.session_state.current_user = username  # 记录当前登录的用户
                    st.success("登录成功！")
                    st.session_state.page = "main"  # 设置页面为主页面
                    st.experimental_rerun()  # 重新运行应用
                else:
                    st.error("用户名或密码错误！")
            elif username or password:
                st.error("用户名或密码不能为空！")
       

    # 第二行：注册和跳过按钮
    button_col = st.columns([1,1,1, 1,1])  # 两列宽度相等

    with button_col[1]:
        if st.button("注册"):
            st.session_state.page = "register"
            st.experimental_rerun()

    with button_col[3]:
        if st.button("跳过", key="skip_button"):
            st.session_state.page = "main"
            st.session_state.logged_in = True
            st.experimental_rerun()


    # # 表单输入
    # username = st.text_input("🥰用户名")
    # password = st.text_input("🥳密码", type="password")

    # # 创建一个包含三个列的布局
    # col1, col2 = st.columns([10, 1])

    # # 登录按钮在第一列
    # with col1:
    #     if st.button("登录"):
    #         if username in st.session_state.users and st.session_state.users[username] == password:
    #             st.session_state.logged_in = True  # 设置登录状态
    #             st.session_state.current_user = username  # 记录当前登录的用户
    #             st.success("登录成功！")
    #             st.session_state.page = "main"  # 设置页面为主页面
    #             st.experimental_rerun()  # 重新运行应用
    #         else:
    #             st.error("用户名或密码错误！")

    # # 注册按钮也在第一列
    # with col1:
    #     if st.button("注册"):
    #         st.session_state.page = "register"
    #         st.experimental_rerun()

    # # 跳过按钮在第三列
    # with col3:
    #     if st.button("跳过", key="skip_button"):
    #         st.session_state.page = "main"
    #         st.session_state.logged_in = True
    #         st.experimental_rerun()
        # 创建一个包含两个列的布局


    # 添加底部标语
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #D3D3D3;
            color: #000000;
            text-align: center;
            padding: 20px;
            font-family: 'Pacifico', cursive;
            font-size: 24px;
        }
        </style>
        <div class="footer">
            An apple a day keeps the doctor away！
        </div>
        """,
        unsafe_allow_html=True
    )

def register_page():

    st.title('寻医问药小管家🩺')

    # 添加注册界面的小标题
    #st.subheader('🙌注册界面')
    # 表单输入
    new_username = st.text_input("🙋🏻‍♂️新用户名")
    new_password = st.text_input("🗝️新密码", type="password")

    # 注册按钮
    if st.button("注册"):
        if new_username in st.session_state.users:
            st.error("用户名已存在！")
        elif new_username and new_password:
            st.session_state.users[new_username] = new_password
            st.success("注册成功，请登录！")
            st.session_state.page = "login"
            st.experimental_rerun()
        else:
            st.error("用户名和密码不能为空！")

    # 返回登录页面按钮
    if st.button("返回登录页面"):
        st.session_state.page = "login"
        st.experimental_rerun()
        # 添加底部标语
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #D3D3D3;
            color: #000000;
            text-align: center;
            padding: 20px;
            font-family: 'Pacifico', cursive;
            font-size: 24px;
        }
        </style>
        <div class="footer">
            An apple a day keeps the doctor away！
        </div>
        """,
        unsafe_allow_html=True
    )
def main_page():
    st.title('寻医问药小管家👨🏻‍⚕️')

    # 初始化对话列表
    if "conversations" not in st.session_state:
        st.session_state.conversations = {"默认对话": {"messages": [], "memory": ConversationBufferMemory(memory_key='chat_history')}} 
        st.session_state.current_conversation = "默认对话"

    # 初始化 selected_model
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "百川"

    # 选择或创建对话
    with st.sidebar:
        conversation_name = st.selectbox("选择对话", list(st.session_state.conversations.keys()) + ["新建对话"],index=len(list(st.session_state.conversations.keys()))-1)
        if conversation_name == "新建对话":
            new_conversation_name = st.text_input("请输入新对话名称")
            if st.button("创建对话") and new_conversation_name:
                st.session_state.conversations[new_conversation_name] = {"messages": [], "memory": ConversationBufferMemory(memory_key='chat_history')}
                st.session_state.current_conversation = new_conversation_name
                st.experimental_rerun()
        else:
            st.session_state.current_conversation = conversation_name

        # 切换对话
        st.write(f"当前对话: {st.session_state.current_conversation}")

        # 删除对话
        delete_conversation_name = st.selectbox("删除对话", ["选择要删除的对话"] + list(st.session_state.conversations.keys()))
        if delete_conversation_name != "选择要删除的对话" and st.button("删除"):
            del st.session_state.conversations[delete_conversation_name]
            if st.session_state.current_conversation == delete_conversation_name:
                st.session_state.current_conversation = None
            st.experimental_rerun()

        # 初始化 selected_model
        if "selected_model" not in st.session_state:
            st.session_state.selected_model = "百川"

        # 下拉菜单选择模型
        model = st.selectbox("选择模型（默认为百川）", ["百川", "智谱", "你自己的选择"], index=["百川", "智谱", "你自己的选择"].index(st.session_state.selected_model))
        st.write(f"你选择了 {model}模型")
        st.session_state.selected_model = model

        # 子页面链接
        if st.button("设置API Key"):
            st.session_state.page = "settings"
            st.experimental_rerun()

        uploaded_file = st.file_uploader("上传文件", type=["txt"])
        if uploaded_file is not None:
            st.write("已上传文件: ", uploaded_file.name)
            # 处理上传的文件（例如：读取文件内容、传输文件等）

            # 解码文件内容为字符串
            try:
                file_content = uploaded_file.read().decode('utf-8')  # 假设文件内容是以UTF-8编码的
            except UnicodeDecodeError:
                st.error("文件解码失败，请上传一个有效的UTF-8编码文件。")
                return

           # with st.chat_message('user', avatar='😣'):
           #     st.markdown(file_content)

            current_conversation["messages"].append({'role': 'user', 'content': file_content})

            # 将解码后的文件内容传递给 generate_response 函数
            response = generate_response(current_conversation["memory"], file_content)
                # 展示聊天记录

            response = response['text']
            current_conversation["messages"].append({'role': 'assistant', 'content': response})

        st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)  # 根据侧边栏高度调整值
        if st.button("返回登录界面"):
            st.session_state.page = "login"
            st.experimental_rerun()

         # 获取当前对话
    current_conversation = st.session_state.conversations.get(st.session_state.current_conversation, None)
    if current_conversation is None:
        st.write("请创建或选择一个对话")
        return           

    #     # 添加返回登录按钮到右下角
    # with back_to_login_placeholder.container():
    #     st.markdown('<div style="position: fixed; bottom: 10px; right: 10px;">', unsafe_allow_html=True)
    # if st.button("返回登录"):
    #     st.session_state.logged_in = False
    #     st.session_state.page = "login"
    #     st.experimental_rerun()
    # st.markdown('</div>', unsafe_allow_html=True)

    # 初始化聊天记录
    #if "messages" not in st.session_state:
    #    st.session_state.messages = []
    #    st.session_state.memory = ConversationBufferMemory(memory_key='chat_history')

    # 展示当前选择的模型
    st.markdown(f"**当前使用的模型: {st.session_state.selected_model}**")



    # 展示聊天记录
    for message in current_conversation["messages"]:
        if message["role"] == "user":
            with st.chat_message(message["role"], avatar='😣'):
                st.markdown(message["content"])
        else:
            with st.chat_message(message["role"], avatar='👨🏻‍⚕️'):
                st.markdown(message["content"])

    # 用于用户输入
    if prompt := st.chat_input('请您说出您不舒服的地方'):
        with st.chat_message('user', avatar='😣'):
            st.markdown(prompt)

        current_conversation["messages"].append({'role': 'user', 'content': prompt})

        answer = generate_response(current_conversation["memory"], prompt,st.session_state.selected_model)

        response = answer['text']

        with st.chat_message('assistant', avatar='👨🏻‍⚕️'):
            st.markdown(response)
        current_conversation["messages"].append({'role': 'assistant', 'content': response})

def settings_page():
    # 初始化API key session state
    if "model_api_keys" not in st.session_state:
        st.session_state.model_api_keys = {
            "百川": "sk-cfdf885592540e8f76134c1cfd962dd0",
            "智谱": "9d46dc29be6a3ea5da64efaf9a7caa41.IMe2UoaxYA4Lrhap",
            "你自己的选择": "your_custom_api_key_here"
        }
        st.session_state.model_urls = {
            "百川": "https://api.baichuan-ai.com/v1",
            "智谱": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
            "你自己的选择": ""
        }
        st.session_state.model_names = {
            "百川": "Baichuan3-Turbo",
            "智谱": "glm-4",
            "你自己的选择": ""
        }

    # 获取当前选择的模型
    model = st.session_state.get("selected_model", "百川")

    st.title(f'设置 {model} 的 API Key')

    # 确保 model 存在于 model_api_keys 中
    if "model_api_keys" not in st.session_state:
        st.session_state.model_api_keys = {
            "你自己的选择": ""
        }
        st.session_state.model_urls = {
            "你自己的选择": ""
        }
        st.session_state.model_names = {
            "你自己的选择": ""
        }
    
    # 输入API key
    api_key = st.text_input(f"{model} API Key", value=st.session_state.model_api_keys.get(model, ""), type='password')
    # 输入API URL
    api_url = st.text_input(f"{model} API URL", value=st.session_state.model_urls.get(model, ""))
    # 输入模型名称
    model_name = st.text_input(f"{model} 模型名称", value=st.session_state.model_names.get(model, ""))

    # 保存按钮
    if st.button("保存"):
        st.session_state.model_api_keys[model] = api_key
        st.session_state.model_urls[model] = api_url
        st.session_state.model_names[model] = model_name
        st.success(f"{model} 的设置已保存")
        # st.session_state.page = "main"
        # st.experimental_rerun()

    # 切换到百川模型
    if model == "百川" and st.button("切换到百川大模型"):
        st.success("已经成功切换到百川大模型")
        st.session_state.selected_model = "百川"
        # st.session_state.page = "main"
        # st.experimental_rerun()
    # 切换到智谱模型
    if model == "智谱" and st.button("切换到智谱大模型"):
        st.success("已经成功切换到智谱大模型")
        st.session_state.selected_model = "智谱"
        # st.session_state.page = "main"
        # st.experimental_rerun()

    # 切换到自定义模型
    if model == "你自己的选择" and st.button("切换到自定义大模型"):
        st.success("已经成功切换到自定义大模型")
        st.session_state.selected_model = "你自己的选择"
        # st.session_state.page = "main"
        # st.experimental_rerun()

    # 返回主页面
    if st.button("返回"):
        st.session_state.page = "main"
        st.experimental_rerun()

def main():
    if "page" not in st.session_state:
        st.session_state.page = "start"

    if st.session_state.page == "start":
        start_page()
    elif st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "register":
        register_page()
    elif st.session_state.page == "main":
        main_page()
    elif st.session_state.page == "settings":
        settings_page()


if __name__ == "__main__":
    main()


