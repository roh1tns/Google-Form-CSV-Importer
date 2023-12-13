import gspread

credentials = {
    "installed":
    {"client_id":"295208202717-6m92s3tj4hlt0st8o0otqqold6i96gtq.apps.googleusercontent.com",
     "project_id":"gsheet-api-400610",
     "auth_uri":"https://accounts.google.com/o/oauth2/auth",
     "token_uri":"https://oauth2.googleapis.com/token",
     "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
     "client_secret":"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",
     "redirect_uris":["http://localhost"]}
     }

gc, authorized_user = gspread.oauth_from_dict(credentials)