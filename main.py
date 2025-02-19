from src.send_email import get_counts, get_or_update_edition, generate_email_template, send_email

def main():
    counts = get_counts()
    print("Contagens obtidas:", counts)

    email_html = generate_email_template(counts)
    edition_number = get_or_update_edition(increment=True)
    recipient_email = "avieira@bvp.com"  

    send_email(recipient_email, email_html, edition_number=edition_number)

if __name__ == "__main__":
    main()
