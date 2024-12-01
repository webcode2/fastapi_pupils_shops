
from .email_includes import html_content_template
def html_content(code,user):
    title="Reset Your Password"
    body=f"""
     <div class="email-body">
            <p>Hello {user},</p>
            <p>Use the following code to reset your password:</p>
            <div class="reset-token">{code}</div>
            <p>Alternatively, click the button below to reset your password:</p>
            <p style="text-align: center;">
                <a href="[Reset Link]" class="cta-button">Reset My Password</a>
            </p>
    """
    body_style="""
    .email-body {
            padding: 20px;
            color: #555;
        }
        .reset-token {
            font-size: 20px;
            font-weight: bold;
            color: #2196F3;
            text-align: center;
            margin: 20px 0;
        }
        .cta-button {
            display: inline-block;
            background: #2196F3;
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
        }
    """
    return html_content_template(body=body,body_style=body_style,title=title)