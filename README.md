How It Works
1. Login: The bot logs in using the provided credentials.
2. Fetch Users: It retrieves a list of users in the specified groups, excluding:
     Users specified in EXCLUDED_USERS
3. Check Activity: It fetches the last edit or log action timestamp for each user.
4. Determine Status:
     Active: Activity within the last 30 days
     Inactive (1 month): No activity in the last 30–60 days
     Inactive (2 months): No activity in the last 60–75 days
     Inactive (2 months, 2 weeks): No activity for more than 75 days
5. Generate Report:
     Displays user activity status in a table
     Lists grace periods only for users inactive for more than 2 months and 2 weeks
