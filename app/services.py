import app.extensions as extensions

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