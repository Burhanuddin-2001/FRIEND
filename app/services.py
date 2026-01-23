import app.extensions as extensions  # <--- Import the module, not the variable

class UserService:
    @staticmethod
    def create_user(email: str, name: str = None):
        """Creates a new user in Supabase."""
        data = {
            "email": email,
            "name": name,
            "is_active": True
        }
        # Access supabase via the module to get the current (mocked) instance
        response = extensions.supabase.table("users_profile").insert(data).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def get_user_by_email(email: str):
        """Finds a user by email."""
        response = extensions.supabase.table("users_profile").select("*").eq("email", email).execute()
        return response.data[0] if response.data else None