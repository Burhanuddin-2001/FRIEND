import app.extensions as extensions
import os
import requests
class UserService:
    @staticmethod
    def sign_up(email: str, password: str, name: str):
        """
        1. Creates auth user in Supabase.
        2. Creates profile entry in our table.
        """
        # 1. Sign up in Supabase Auth
        auth_response = extensions.supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        
        if not auth_response.user:
            raise Exception("Failed to create auth user")

        user_id = auth_response.user.id

        # 2. Create profile in our public table
        data = {
            "id": user_id,
            "email": email,
            "name": name,
            "is_active": True
        }
        extensions.supabase.table("users_profile").insert(data).execute()
        return auth_response.user

    @staticmethod
    def sign_in(email: str, password: str):
        """Signs in and returns the session/user."""
        response = extensions.supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response

    @staticmethod
    def get_profile(user_id: str):
        """Get the public profile details."""
        response = extensions.supabase.table("users_profile").select("*").eq("id", user_id).execute()
        return response.data[0] if response.data else None
    
class AIService:
    @staticmethod
    def generate_message(user_name: str):
        """
        Generates a warm, short email body using Priyanshu API.
        """
        api_key = os.environ.get("PRIYANSHU_API_KEY")
        if not api_key:
            return "Error: AI API Key missing."

        url = "https://priyanshuapi.xyz/api/runner/priyanshu-ai"
        
        # Strict prompt to keep the AI in character
        system_instruction = (
            "You are writing a short email to a friend. "
            "Keep it warm, human, and casual. No motivational clichés. "
            "No direct advice unless gentle. 2–5 sentences maximum. "
            "Do not mention AI, systems, or automation. "
            "Sign off simply."
        )
        
        user_prompt = f"Write a short email to my friend named {user_name}."

        payload = {
            "prompt": user_prompt,  # The API seems to require this field
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ],
            "model": "priyansh-ai"
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status() # Raise error if status is 4xx or 5xx
            
            data = response.json()
            
            # Parse the specific response structure you provided
            # data['data']['choices'][0]['message']['content']
            content = data.get("data", {}).get("choices", [])[0].get("message", {}).get("content", "")
            
            return content.strip()
            
        except Exception as e:
            print(f"AI Generation Error: {e}")
            # Fallback message in case AI fails
            return f"Hey {user_name}, just thinking of you today. Hope you're doing well!"