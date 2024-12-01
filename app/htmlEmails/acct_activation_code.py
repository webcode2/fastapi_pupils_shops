from .import app_details
from  .email_includes import html_content_template
def html_content(code,user):
    style="""
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

    """
    body=f"""
            <div class="email-body">
            <p>Hi {user},</p>
            <p>Thank you for signing up with the {app_details.app_name}! We're excited to have you on board. To complete your registration, please verify your email address using the code below:</p>
            <div class="verification-code">{code}</div>
            <p>If you didn't sign up for [Your Service Name], you can safely ignore this email.</p>
            <p>Alternatively, click the button below to verify your account:</p>
            <p style="text-align: center;">
                <a href="[Verification Link]" class="cta-button">Verify My Account</a>
            </p>
        </div>

    """
    title=f"""
    Welcome to  {app_details.app_name}!"""
    return html_content_template(body=body,body_style=style,title=title)