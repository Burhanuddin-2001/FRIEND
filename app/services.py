import os
import requests
import random
import resend
import re  # <--- Added Regex for surgical cleaning
import app.extensions as extensions

class UserService:
    @staticmethod
    def sign_up(email: str, password: str, name: str):
        """Creates auth user in Supabase and profile in DB."""
        auth_response = extensions.supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        
        if not auth_response.user:
            raise Exception("Failed to create auth user")

        user_id = auth_response.user.id

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
        return extensions.supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

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
        Enforces strict cleaning to remove placeholders.
        """
        api_key = os.environ.get("PRIYANSHU_API_KEY")
        if not api_key:
            return "Error: AI API Key missing."

        url = "https://priyanshuapi.xyz/api/runner/priyanshu-ai"
        
        # Creative sign-offs
        sign_offs = [
            "Your best pal", 
            "The seat sharer", 
            "The scribble maker", 
            "Your partner in crime", 
            "From the other side of the screen",
            "Yours truly",
            "The chaos coordinator"
        ]
        chosen_sign_off = random.choice(sign_offs)

        # 1. SYSTEM PROMPT
        # We explicitly tell it NOT to sign off. We will handle that.
        system_instruction = (
            f"You are a close friend writing to {user_name}. "
            "TASK: Write a short, warm email body (2-3 sentences). "
            "RULES: "
            "1. Start with 'Hey' or 'Hi'. "
            "2. Do NOT write a Subject line. "
            "3. Do NOT sign off. Do NOT write 'Best', 'Cheers', or '[Your Name]'. Stop after the last sentence. "
            "4. Include a specific, made-up memory (e.g., 'that time we got lost', 'the coffee shop incident'). "
            "5. Keep it casual and lower-case friendly."
        )
        
        user_prompt = f"Write a short message to {user_name} about a random shared memory."

        payload = {
            "prompt": user_prompt,
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
            response.raise_for_status()
            
            data = response.json()
            content = data.get("data", {}).get("choices", [])[0].get("message", {}).get("content", "")
            
            # --- SURGICAL CLEANING (The "Rubix" Logic) ---
            
            # 1. Remove "Subject: ..." lines entirely
            content = re.sub(r"(?i)Subject:.*?\n", "", content)
            
            # 2. Remove placeholders like [Your Name], [Name], [Date]
            content = re.sub(r"\[.*?\]", "", content)
            
            # 3. Remove common sign-off triggers if the AI ignored us
            # We remove "Best,", "Cheers,", "Sincerely," and anything following them at the end of string
            content = re.sub(r"(?i)(Best|Cheers|Sincerely|Regards|Love),.*$", "", content, flags=re.DOTALL)
            
            # 4. Remove the specific name "Priyanshu" if it appears
            content = content.replace("Priyanshu", "")

            # 5. Final Trim
            content = content.strip()
            
            # 6. Append OUR signature
            final_message = f"{content}\n\n{chosen_sign_off}"
            
            return final_message
            
        except Exception as e:
            print(f"AI Generation Error: {e}")
            return f"Hey {user_name}, just thinking of you today. Hope you're doing well!\n\n{chosen_sign_off}"

class EmailService:
    # (This class remains unchanged from Chapter 05)
    @staticmethod
    def send_email(to_email: str, subject: str, body_html: str, user_id: str = None):
        
        api_key = os.environ.get("RESEND_API_KEY")
        from_email = os.environ.get("FROM_EMAIL", "onboarding@resend.dev")
        
        if not api_key:
            print("Error: RESEND_API_KEY missing.")
            return False

        resend.api_key = api_key

        try:
            params = {
                "from": "Friend <" + from_email + ">",
                "to": [to_email],
                "subject": subject,
                "html": body_html,
            }
            email_response = resend.Emails.send(params)
            
            if user_id:
                log_data = {
                    "user_id": user_id,
                    "subject": subject,
                    "body": body_html,
                    "provider_response": email_response
                }
                extensions.supabase.table("email_logs").insert(log_data).execute()
            return True
        except Exception as e:
            print(f"Email Send Error: {e}")
            return False