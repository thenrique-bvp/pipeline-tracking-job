from src.send_email import get_counts, generate_email_template, send_email

def main():
    counts = get_counts()
    print("Contagens obtidas:", counts)

    email_html = generate_email_template(counts)

    recipient_email = "avieira@bvp.com"  

    send_email(recipient_email, email_html)

if __name__ == "__main__":
    main()
