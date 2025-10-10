import streamlit as st
from session_manager import SessionManager
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 初始化會話管理器
if 'session_manager' not in st.session_state:
    st.session_state.session_manager = SessionManager()

# 初始化當前選中的會話
if 'current_session_id' not in st.session_state:
    st.session_state.current_session_id = None

# 頁面標題
st.title("🦆 小鴨聊天機器人")
st.markdown("---")

# 側邊欄 - 會話管理
with st.sidebar:
    st.header("會話管理")
    
    # 新增會話
    st.subheader("新增會話")
    new_session_name = st.text_input("會話名稱", placeholder="輸入會話名稱（可選）")
    if st.button("➕ 創建新會話", use_container_width=True):
        session_id = st.session_state.session_manager.create_session(new_session_name)
        st.session_state.current_session_id = session_id
        st.success(f"已創建會話：{new_session_name or '新會話'}")
        st.rerun()
    
    st.markdown("---")
    
    # 會話列表
    st.subheader("會話列表")
    sessions = st.session_state.session_manager.get_sessions()
    
    if not sessions:
        st.info("尚無會話，請先創建一個會話")
    else:
        for session_id, session_info in sessions.items():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # 會話選擇按鈕
                if st.button(
                    f"💬 {session_info['name']}", 
                    key=f"select_{session_id}",
                    use_container_width=True,
                    type="primary" if session_id == st.session_state.current_session_id else "secondary"
                ):
                    st.session_state.current_session_id = session_id
                    st.rerun()
            
            with col2:
                # 刪除會話按鈕
                if st.button(
                    "🗑️", 
                    key=f"delete_{session_id}",
                    help="刪除會話"
                ):
                    st.session_state.session_manager.delete_session(session_id)
                    if st.session_state.current_session_id == session_id:
                        st.session_state.current_session_id = None
                    st.success(f"已刪除會話：{session_info['name']}")
                    st.rerun()

# 主要內容區域
if st.session_state.current_session_id is None:
    st.info("請從左側選擇或創建一個會話開始聊天")
else:
    current_session = sessions[st.session_state.current_session_id]
    st.subheader(f"當前會話：{current_session['name']}")
    
    # 顯示聊天記錄
    messages = st.session_state.session_manager.get_session_messages(st.session_state.current_session_id)
    
    # 聊天記錄容器
    chat_container = st.container()
    
    with chat_container:
        if not messages:
            st.info("開始與小鴨聊天吧！它會用可愛的方式回應你。")
        else:
            for msg in messages:
                # 使用者訊息
                with st.chat_message("user"):
                    st.write(msg['user'])
                
                # 助手回應
                with st.chat_message("assistant"):
                    st.write(msg['assistant'])
    
    # 訊息輸入
    st.markdown("---")
    
    # 使用 form 來處理訊息發送
    with st.form(key="message_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_input(
                "輸入訊息", 
                placeholder="輸入你想說的話...",
                label_visibility="collapsed"
            )
        
        with col2:
            send_button = st.form_submit_button("發送", use_container_width=True)
    
    # 處理訊息發送
    if send_button and user_input.strip():
        try:
            # 在聊天容器中立即顯示新訊息
            with chat_container:
                # 顯示用戶訊息
                with st.chat_message("user"):
                    st.write(user_input.strip())
                
                # 顯示助手回應
                with st.chat_message("assistant"):
                    response_placeholder = st.empty()
                    response_placeholder.write("🦆 小鴨正在思考中...")
                    
                    try:
                        # 使用串流回應
                        full_response = ""
                        for partial_response in st.session_state.session_manager.send_message(st.session_state.current_session_id, user_input.strip()):
                            full_response = partial_response
                            response_placeholder.write(partial_response + " ▋")
                        
                        # 完成回應，移除游標
                        response_placeholder.write(full_response)
                        
                    except Exception as e:
                        # 顯示錯誤訊息
                        response_placeholder.write("🦆 呱呱～小鴨遇到了一些問題 (小鴨很抱歉)")
            
            # 重新載入以顯示完整的聊天記錄
            st.rerun()
            
        except Exception as e:
            st.error(f"發送訊息時發生錯誤：{str(e)}")

# 頁腳資訊
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        🦆 這是一個可愛的小鴨聊天機器人，它會用幽默的方式回應你
    </div>
    """, 
    unsafe_allow_html=True
)