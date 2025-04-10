IMPORTANT NOTICE : THIS CODE DOES NOT HANDLE ERRORS, USE WITH CAUTION
Note : Since I run my bot locally on my own machine, I don't use environment variables that's why you see that I hard coded the username and password in this code.

This bot generates an inactivity report for administrators, bureaucrats, interface administrators, and non-steward suppressors on TestWiki. It checks the last activity of users in these roles and categorizes them based on their activity status. The report is then posted to https://testwiki.wiki/wiki/Activity

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
