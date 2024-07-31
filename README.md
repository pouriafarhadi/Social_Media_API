# BLOG API Endpoints

| Name                             | Description                                                        | URL                                                   | Method    | Params              |
|----------------------------------|--------------------------------------------------------------------|-------------------------------------------------------|-----------|---------------------|
| Home page with all posts         | Returns all posts                                                  | **/blog/posts/**                                      | GET       |                     |
| All posts of a specific user     | Returns all posts of the specified user                            | **/blog/posts/user/<user_id>/**                       | GET       |                     |
| All of my posts                  | Returns all posts authored by the authenticated user               | **/blog/posts/mine/**                                 | GET       |                     |
| Posts of following user profiles | Returns posts from the profiles followed by the authenticated user | **/blog/posts/followings/**                           | GET       |                     |
| Post detail view                 | Returns the details of a specific post                             | **/blog/posts/<post_id>/info/**                       | GET       |                     |
| Update post                      | Updates a specific post (authenticated and post author only)       | **/blog/posts/<post_id>/**                            | PUT/PATCH | title, content      |
| Delete post                      | Deletes a specific post (authenticated and post author only)       | **/blog/posts/<post_id>/**                            | DELETE    |                     |
| Create post                      | Creates a new post                                                 | **/blog/posts/**                                      | POST      | title, content      |
| Like/unlike post                 | Likes or unlikes a specific post                                   | **/blog/posts/<post_id>/like/**                       | POST      |                     |
| Save/unsave post                 | Saves or unsaves a specific post                                   | **/blog/posts/<post_id>/save/**                       | POST      |                     |
| View post comments               | Returns all comments for a specific post                           | **/blog/posts/<post_id>/comments/**                   | GET       |                     |
| Create post comment              | Creates a new comment for a specific post                          | **/blog/posts/<post_id>/comments/**                   | POST      | comment_body, reply |
| Like/unlike post comment         | Likes or unlikes a specific comment                                | **/blog/posts/<post_id>/comments/<comment_id>/like/** | POST      |                     |
| Liked posts                      | Returns all posts liked by the authenticated user                  | **/blog/posts/liked/**                                | GET       |                     |
| Saved posts                      | Returns all posts saved by the authenticated user                  | **/blog/posts/saved/**                                | GET       |                     |
| Search posts                     | Searches posts by title or author's username                       | **/blog/posts/search/?q=<search_query>**              | GET       |                     |

**Note:** All endpoints require the user to be authenticated. Replace `<user_id>`, `<post_id>`, `<comment_id>`,
and `<search_query>` with the appropriate values when making requests.

# NETWORK API Endpoints

| Name                  | Description                                                                          | URL                                                             | Method | Params                                                   |
|-----------------------|--------------------------------------------------------------------------------------|-----------------------------------------------------------------|--------|----------------------------------------------------------|
| Send friend request   | Sends a friend request to another user                                               | **/network/friend_request/**                                    | POST   | receiver_user_id should be sent in the body              |
| Friend requests list  | Returns a list of friend requests (both sent and received by the authenticated user) | **/network/friend_request/**                                    | GET    |                                                          |
| Cancel friend request | Cancels a friend request                                                             | **/network/friend_request/<friend_request_object_id>/cancel/**  | POST   | friend_request_object_id provided in friend request list |
| Accept friend request | Accepts a friend request                                                             | **/network/friend_request/<friend_request_object_id>/accept/**  | POST   | friend_request_object_id provided in friend request list |
| Reject friend request | Rejects a friend request                                                             | **/network/friend_request/<friend_request_object_id>/decline/** | POST   | friend_request_object_id provided in friend request list |
| Friend list           | Returns a list of friends                                                            | **/network/friend_list/**                                       | GET    |                                                          |
| Remove friend         | Removes a friend from the friend list                                                | **/network/friend_list/<friendlist_object_id>/unfriend/**       | POST   | friendlist_object_id provided in friend list             |
| Suggest friends       | Returns a list of suggested friends                                                  | **/network/suggest_friend/**                                    | GET    |                                                          |

**Note:** All endpoints require the user to be authenticated. Replace `<friend_request_object_id>`
and `<friendlist_object_id>` with the appropriate values when making requests.

# USERS API Endpoints

| Name                      | Description                                       | URL                             | Method | Params                                            |
|---------------------------|---------------------------------------------------|---------------------------------|--------|---------------------------------------------------|
| Follow users              | Follow a user (authenticated)                     | **/users/profiles/follow/**     | POST   | user_id should be sent in the body of the request |
| Unfollow users            | Unfollow a user (authenticated)                   | **/users/profiles/unfollow/**   | POST   | user_id should be sent in the body of the request |
| Following list of users   | List of users the authenticated user is following | **/users/profiles/followings/** | GET    |                                                   |
| Followers list of users   | List of users following the authenticated user    | **/users/profiles/followers/**  | GET    |                                                   |
| View user profile details | View profile details of the authenticated user    | **/users/profiles/me/**         | GET    |                                                   |

# DJOSER Authentication Endpoints

| Name                   | Description             | URL                                     | Method | Params                                           |
|------------------------|-------------------------|-----------------------------------------|--------|--------------------------------------------------|
| User registration      | Register a new user     | **/auth/users/**                        | POST   | username, password, first_name, last_name, email |
| User activation        | Activate a user account | **/auth/users/activation/**             | POST   | uid, token                                       |
| Resend activation      | Resend activation email | **/auth/users/resend_activation/**      | POST   | username                                         |
| Set password           | Set a new password      | **/auth/users/set_password/**           | POST   | current_password, new_password                   |
| Reset password         | Reset user password     | **/auth/users/reset_password/**         | POST   | username                                         |
| Confirm password reset | Confirm password reset  | **/auth/users/reset_password_confirm/** | POST   | uid, token, new_password                         |
| User login             | Obtain JWT token        | **/auth/jwt/create/**                   | POST   | username, password                               |
| User logout            | Logout user             | **/auth/jwt/destroy/**                  | POST   |                                                  |
| JWT token refresh      | Refresh JWT token       | **/auth/jwt/refresh/**                  | POST   | refresh                                          |

**Note:** All endpoints require the user to be authenticated unless specified otherwise.