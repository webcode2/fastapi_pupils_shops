from .app_details import  app_support_email,app_name

def html_content_template(title,body,body_style):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verify Your Email</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }}
        .email-container {{
            max-width: 600px;
            margin: 20px auto;
            background: #ffffff;
            border: 1px solid #ddd;
            border-radius: 8px;
        }}
        
        .email-header {{
            background-color: #4CAF50;
            color: white;
            text-align: center;
            padding: 20px 10px;
        }}
        .email-body {{
            padding: 20px;
            color: #555;
            line-height: 1.6;
        }}
        .verification-code {{
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
            text-align: center;
            margin: 20px 0;
        }}
        .cta-button {{
            display: inline-block;
            background: #4CAF50;
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
            margin: 20px 0;
        }}
         .footer {{
            text-align: center;
            font-size: 12px;
            color: #aaa;
            padding: 10px 20px;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <!-- Header -->
        <div class="email-header">
            <h1>{title} </h1>
        </div>      
        <!-- Body -->
        
        {body}
        
        <!-- footer -->
        <div class="footer">
            <p>If you have any questions, feel free to contact us at <a href="mailto:{app_support_email}">{app_support_email}</a>.</p>
            <p>&copy; 2024 {app_name}. All rights reserved.</p>
        </div>    </div>
</body>
</html>
"""
