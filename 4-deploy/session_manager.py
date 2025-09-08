import uuid
import asyncio
from typing import Dict, List
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from duck_agent import duck_agent

class SessionManager:
    def __init__(self):
        self.session_service = InMemorySessionService()
        self.app_name = "Parrot Chat App"
        self.user_id = "default_user"  # 固定的使用者 ID
        self.sessions: Dict[str, dict] = {}  # 儲存 session 資訊
        
    def create_session(self, session_name: str = None) -> str:
        """創建新的會話"""
        session_id = str(uuid.uuid4())
        
        # 使用 asyncio.run 來執行 async 方法
        session = asyncio.run(self.session_service.create_session(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=session_id,
            state={}  # 空的初始狀態
        ))
        
        # 儲存會話資訊
        self.sessions[session_id] = {
            'name': session_name or f"會話 {len(self.sessions) + 1}",
            'messages': []
        }
        
        return session_id
    
    def delete_session(self, session_id: str) -> bool:
        """刪除會話"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def get_sessions(self) -> Dict[str, dict]:
        """取得所有會話"""
        return self.sessions
    
    def send_message(self, session_id: str, message: str):
        """發送訊息到指定會話並返回串流回應"""
        import time
        
        if session_id not in self.sessions:
            raise ValueError(f"會話 {session_id} 不存在")
        
        # 創建 Runner
        runner = Runner(
            agent=duck_agent,
            app_name=self.app_name,
            session_service=self.session_service,
        )
        
        # 創建訊息
        new_message = types.Content(
            role="user", 
            parts=[types.Part(text=message)]
        )
        
        # 執行對話並產生串流回應
        full_response = ""
        response_received = False
        
        for event in runner.run(
            user_id=self.user_id,
            session_id=session_id,
            new_message=new_message,
        ):
            if event.content and event.content.parts:
                full_response = event.content.parts[0].text
                response_received = True
                
                # 模擬逐字顯示效果
                words = full_response.split()
                current_text = ""
                for i, word in enumerate(words):
                    current_text += word + " "
                    yield current_text.strip()
                    time.sleep(0.05)  # 短暫延遲以創造打字效果
        
        # 如果沒有收到回應，提供預設回應
        if not response_received:
            full_response = "🦆 呱呱～小鴨暫時說不出話來 (小鴨有點害羞)"
            yield full_response
        
        # 儲存最終訊息記錄
        self.sessions[session_id]['messages'].append({
            'user': message,
            'assistant': full_response
        })
    
    def get_session_messages(self, session_id: str) -> List[dict]:
        """取得會話的訊息記錄"""
        if session_id in self.sessions:
            return self.sessions[session_id]['messages']
        return []