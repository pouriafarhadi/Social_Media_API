# USERS:

| Name                      | Description      | URL                             | Method | Params                                            |
|---------------------------|------------------|---------------------------------|--------|---------------------------------------------------|
| Follow users              | is authenticated | **/users/profiles/follow/**     | POST   | user_id should be sent in the body of the request |
| Unfollow users            | is authenticated | **/users/profiles/unfollow/**   | POST   | user_id should be sent in the body of the request |
| Following list of users   | is authenticated | **/users/profiles/followings/** | GET    |                                                   |
| Followers list of users   | is authenticated | **/users/profiles/followers/**  | GET    |                                                   |
| View user profile details | is authenticated | **/users/profiles/me/**         | GET    |                                                   |

# NOTIFICATIONS:

* [ ] show notifications
