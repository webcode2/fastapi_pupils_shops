from .email_includes import html_content_template

def html_content(user):
    title="""Password Reset Successful"""
    body=f"""
     <div class="email-body">
            <p>Hello {user},</p>
            <p>Your password has been successfully reset. You can now log in with your new password.</p>
            <p>If you didn't perform this action, please contact us immediately.</p>
        </div>
    """
    body_style=""
    return html_content_template(body=body,body_style=body_style,title=title)