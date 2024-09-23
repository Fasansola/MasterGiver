# In your Django app directory, update the file:
# your_app/management/commands/add_skills.py

from django.core.management.base import BaseCommand
from your_app.models import Skill  # Replace 'your_app' with your actual app name

class Command(BaseCommand):
    help = 'Adds a comprehensive list of skills to the database'

    def handle(self, *args, **kwargs):
        skills = [
            # Digital Skills
            "Web Development", "Front-end Development", "Back-end Development",
            "Full-stack Development", "Mobile App Development", "Web Design",
            "UI Design", "UX Design", "Graphic Design", "Logo Design",
            "Illustration", "Animation", "3D Modeling", "Game Design",
            "Content Writing", "Copywriting", "Technical Writing", "Blogging",
            "Social Media Management", "Digital Marketing", "Email Marketing",
            "Search Engine Optimization (SEO)", "Search Engine Marketing (SEM)",
            "Pay-Per-Click (PPC) Advertising", "Content Marketing",
            "Affiliate Marketing", "Influencer Marketing", "Video Production",
            "Video Editing", "Photography", "Photo Editing", "Podcast Production",
            "Audio Editing", "Voice-over", "Data Analysis", "Data Visualization",
            "Machine Learning", "Artificial Intelligence", "Blockchain Development",
            "Cybersecurity", "Network Administration", "Cloud Computing",
            "DevOps", "Quality Assurance", "Software Testing", "User Research",
            "A/B Testing", "Conversion Rate Optimization", "E-commerce Development",
            "Customer Relationship Management (CRM)",
            
            # Business and Management Skills
            "Project Management", "Agile Methodology", "Scrum Master",
            "Product Management", "Business Analysis", "Strategic Planning",
            "Operations Management", "Supply Chain Management",
            "Logistics Management", "Human Resources Management",
            "Talent Acquisition", "Performance Management",
            "Training and Development", "Change Management", "Risk Management",
            "Quality Management", "Event Planning", "Public Relations",
            "Crisis Management", "Brand Management", "Market Research",
            "Competitive Analysis", "Business Development", "Sales",
            "Customer Service", "Fundraising", "Grant Writing",
            "Proposal Writing", "Crowdfunding", "Sponsorship Acquisition",
            "Donor Relations", "Volunteer Coordination", "Non-profit Management",
            "Board Management", "Corporate Social Responsibility",
            "Sustainability Management", "Social Entrepreneurship",
            "Financial Management", "Budgeting", "Accounting", "Bookkeeping",
            "Tax Planning", "Audit", "Investment Management", "Legal Consulting",
            "Contract Negotiation", "Intellectual Property Management",
            "Compliance Management", "Policy Development", "Lobbying",
            
            # Creative and Communication Skills
            "Creative Writing", "Journalism", "Editing", "Proofreading",
            "Translation", "Interpretation", "Public Speaking",
            "Presentation Skills", "Teaching", "Tutoring",
            "Curriculum Development", "Instructional Design",
            "E-learning Development", "Workshop Facilitation",
            "Motivational Speaking", "Storytelling", "Scriptwriting",
            "Speechwriting", "Brand Storytelling", "Visual Storytelling",
            
            # Physical and Practical Skills
            "Carpentry", "Plumbing", "Electrical Work", "Painting",
            "Landscaping", "Gardening", "Construction", "Home Repair",
            "Auto Mechanics", "Bicycle Repair", "Sewing", "Knitting",
            "Cooking", "Baking", "Nutrition Planning", "Fitness Training",
            "Yoga Instruction", "Dance Instruction", "Music Instruction",
            "Art Instruction", "Sports Coaching", "First Aid", "CPR",
            "Disaster Response", "Search and Rescue", "Animal Care",
            "Pet Grooming", "Wildlife Conservation",
            "Environmental Conservation", "Recycling and Waste Management",
            
            # Interpersonal and Social Skills
            "Counseling", "Mentoring", "Life Coaching", "Career Coaching",
            "Conflict Resolution", "Mediation", "Negotiation", "Team Building",
            "Leadership Development", "Diversity and Inclusion Training",
            "Cultural Sensitivity Training", "Sign Language", "Child Care",
            "Elder Care", "Special Needs Support", "Crisis Intervention",
            "Suicide Prevention", "Addiction Support", "Mental Health Support",
            "Grief Counseling",
            
            # Specialized Professional Skills
            "Architecture", "Urban Planning", "Interior Design",
            "Fashion Design", "Industrial Design", "Product Design",
            "Sustainable Design", "Renewable Energy Engineering",
            "Environmental Engineering", "Biomedical Engineering",
            "Mechanical Engineering", "Electrical Engineering",
            "Civil Engineering", "Chemical Engineering", "Aerospace Engineering",
            "Agricultural Science", "Food Science", "Nutrition Science",
            "Environmental Science", "Marine Biology", "Geology", "Meteorology",
            "Astronomy", "Physics", "Chemistry", "Biology", "Genetics",
            "Microbiology", "Epidemiology", "Public Health", "Pharmacology",
            "Veterinary Medicine", "Dentistry", "Optometry", "Physical Therapy"
        ]

        for skill_name in skills:
            skill, created = Skill.objects.get_or_create(name=skill_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added skill: {skill_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Skill already exists: {skill_name}'))

        self.stdout.write(self.style.SUCCESS(f'Finished adding {len(skills)} skills'))