from src.pipeline_tracking_job import get_user_rules, get_all_companies_updates, filter_updates_by_rules, create_email_template, send_email
import requests


def main():
    try:
        response = requests.get(
            "https://brain.bessemer.io/twitter/tracking/emails")
        data = response.json()
        emails = data.get("emails", [])
    except (requests.exceptions.RequestException) as e:
        print(f"Error fetching emails: {e}")
        emails = []

    # emails = ["famorim@bvp.com"]
    # Process each email
    for email in emails:
        try:
            print(f"\nProcessing email: {email}")
            rules = get_user_rules(email)

            if not rules:
                print(f"No rules found for email: {email}")
                continue

            # Obter todas as atualizações do usuário
            all_updates = get_all_companies_updates(str(email))
            filtered_updates = filter_updates_by_rules(all_updates, rules)

            if len(filtered_updates) > 0:
                html_content = create_email_template(filtered_updates)
                send_email("thenrique@bvp.com", html_content)
                send_email("famorim@bvp.com", html_content)
                send_email("avieira@bvp.com", html_content)
                print(filtered_updates)
                return filtered_updates
            else:
                print(f"No updates found for {email}")
                return []
        except Exception as e:
            print(f"Error processing {email}: {e}")
            continue


if __name__ == "__main__":
    main()
