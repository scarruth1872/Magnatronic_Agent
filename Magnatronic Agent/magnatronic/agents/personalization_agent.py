from magnatronic.core.agent import Agent
from magnatronic.core.tasks import task

class PersonalizationAgent(Agent):
    def __init__(self):
        super().__init__(name='personalization')
        self.user_preferences = {}
        self.user_profiles = {}

    @task
    def learn_preferences(self, user_id, interaction_data):
        """Learn and update user preferences based on interaction data."""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {}
        
        # Update preferences based on interaction data
        for key, value in interaction_data.items():
            if key in self.user_preferences[user_id]:
                # Update existing preference with weighted average
                self.user_preferences[user_id][key] = (
                    0.7 * self.user_preferences[user_id][key] + 0.3 * value
                )
            else:
                # Initialize new preference
                self.user_preferences[user_id][key] = value
        
        return self.user_preferences[user_id]

    @task
    def get_recommendations(self, user_id, context):
        """Generate personalized recommendations based on user preferences."""
        if user_id not in self.user_preferences:
            return []
        
        preferences = self.user_preferences[user_id]
        # Generate recommendations based on preferences and context
        recommendations = [
            item for item in context
            if self._match_preferences(item, preferences)
        ]
        
        return sorted(recommendations, key=lambda x: x.get('relevance', 0), reverse=True)

    @task
    def update_profile(self, user_id, profile_data):
        """Update user profile with new information."""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {}
        
        # Update profile fields
        self.user_profiles[user_id].update(profile_data)
        return self.user_profiles[user_id]

    @task
    def get_profile(self, user_id):
        """Retrieve user profile information."""
        return self.user_profiles.get(user_id, {})

    def _match_preferences(self, item, preferences):
        """Helper method to match items against user preferences."""
        relevance = 0
        for key, value in preferences.items():
            if key in item:
                relevance += abs(item[key] - value)
        
        item['relevance'] = 1 / (1 + relevance)  # Normalize relevance score
        return True  # Include all items with relevance score