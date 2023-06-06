# Cloud_Native_Finals_Term_10

## User Story
1. As a company employee, I want to be able to browse publicly available documents so that I can access important information.
2. As a department member, I want to be able to maintain and edit documents that are relevant to my team so that I can collaborate effectively with my colleagues.
3. As a user, I want to be able to maintain and edit my own personal documents so that I can keep track of my own work.
4. As a user, I want to be able to delete my own personal documents in case they are no longer relevant.
5. As a user, I want to be able to view the version history of a document so that I can see who made what changes at what time and review previous versions of the document.
6. As a user, I want to be able to see a snapshot of a document at a specific point in time so that I can compare it to the current version or review previous versions.


## UI Design 

## System Architecture
![image](https://github.com/Joechen0130/Cloud_Native_Finals_Term_10/assets/62683955/a5dfa3cd-6ed6-4b36-9dc6-e39abdc9a36d)
![image](https://github.com/Joechen0130/Cloud_Native_Finals_Term_10/assets/62683955/22af2762-5d56-415c-868c-86c2b32c3546)

## Application Implementation
Database
- SQlite:
  - user、files
- Model:
  - user 、title 、description、filepath、date_created、date_updated
- View:
  - home、register_user、manage_post、delete / save post、history data、public、update pass word
- Template:
  - home.html、log_in.html、history.html、public.html、history.html、manage_post.html、base.html
- Static: bootstrap、font awesome
- Media: logo (tsmc)

## Testing
![image](https://github.com/Joechen0130/Cloud_Native_Finals_Term_10/assets/62683955/49d5c55c-e8a9-4209-b51c-30c97a086642)
- Test Case
  - URL test
  - Register test
  - Login test
  - Edit profile test
  - Change password test
  - Upload file test
  - Delete file test
  - Change file test
 



