from .email_includes  import html_content_template
def html_content(user,code):
    title=f"""Password Reset Request"""
    body=f""" <div class="email-body">
            <p>Hello {user},</p>
            <p>We received a request to reset your password. If you made this request, click the button below to reset your password:</p>
            <p style="text-align: center;">
                <a href="[Reset Link]" class="cta-button">Reset My Password</a>
            </p>
            <p>If you didn't request a password reset, you can safely ignore this email.</p>
        </div>
        """
    return html_content_template(body_style="",title=title,body=body,)

