import streamlit as st
from langchain.memory import ConversationBufferMemory
from chain import generate_response, build_chain

# 假设的用户名和密码存储
if "users" not in st.session_state:
    st.session_state.users = {"user": "password"}

def login_page():
    st.title('👋登录界面')

    # 表单输入
    username = st.text_input("🙋🏻‍♂️用户名")
    password = st.text_input("🗝️密码", type="password")

    # 登录按钮
    if st.button("登录"):
        if (username in st.session_state.users 
            and st.session_state.users[username] == password):
            st.session_state.logged_in = True  # 设置登录状态
            st.session_state.current_user = username  # 记录当前登录的用户
            st.success("登录成功！")
            st.session_state.page = "main"  # 设置页面为主页面
            st.experimental_rerun()  # 重新运行应用
        else:
            st.error("用户名或密码错误！")

    # 注册按钮
    if st.button("注册"):
        st.session_state.page = "register"
        st.experimental_rerun()

    # 添加跳过按钮
    header_placeholder = st.empty()
    with header_placeholder.container():
        col1, col2 = st.columns([9, 1])
        with col1:
            st.write("")
        with col2:
            if st.button("跳过", key="skip_button"):
                st.session_state.page = "main"
                st.session_state.logged_in = True
                st.experimental_rerun()

def register_page():
    st.title("注册界面")

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

def main_page():
    st.title('中软人质的寻医问药机器人👨‍⚕️')

    # 设置侧边栏
    with st.sidebar:
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

        # 注销按钮
        if st.button("注销"):
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.experimental_rerun()

    # 初始化聊天记录
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.memory = ConversationBufferMemory(memory_key='chat_history')

    # 展示当前选择的模型
    st.markdown(f"**当前使用的模型: {st.session_state.selected_model}**")

    # 展示聊天记录
    for message in st.session_state.messages:
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

        st.session_state.messages.append({'role': 'user', 'content': prompt})

        chain = build_chain(st.session_state.memory, model_type=st.session_state.selected_model)

        answer = generate_response(chain, prompt)

        response = answer['text']

        with st.chat_message('assistant', avatar='👨🏻‍⚕️'):
            st.markdown(response)
        st.session_state.messages.append({'role': 'assistant', 'content': response})

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
        st.session_state.page = "main"
        st.experimental_rerun()

    # 切换模型按钮
    if st.button(f"切换到 {model} 大模型"):
        st.success(f"已经成功切换到 {model} 大模型")
        st.session_state.selected_model = model
        st.session_state.page = "main"
        st.experimental_rerun()

    # 返回主页面
    if st.button("返回"):
        st.session_state.page = "main"
        st.experimental_rerun()

# 初始化 session_state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"  # 默认页面为登录页面

# 根据 page 变量决定显示哪个页面
if st.session_state.page == "main":
    if st.session_state.logged_in:
        main_page()
    else:
        login_page()
elif st.session_state.page == "login":
    login_page()
elif st.session_state.page == "register":
    register_page()
elif st.session_state.page == "settings":
    settings_page()
