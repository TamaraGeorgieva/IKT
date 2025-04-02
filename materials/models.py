from django.db import models
from django.core.validators import FileExtensionValidator
from Quiz_app.accounts.models import User


class Document(models.Model):
    DOCUMENT_TYPES = (
        ('pdf', 'PDF'),
        ('docx', 'Word'),
        ('gdoc', 'Google Doc'),
    )

    title = models.CharField(max_length=255)
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPES)
    file = models.FileField(
        upload_to='documents/',
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'doc', 'docx'],
                message="Only PDF or Word documents are allowed"
            )
        ]
    )
    google_doc_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Only required for Google Docs"
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.document_type == 'pdf' and self.file and not self.file.name.lower().endswith('.pdf'):
            raise ValidationError("PDF document type requires a .pdf file")

        if self.document_type == 'docx' and self.file and not any(
                self.file.name.lower().endswith(ext) for ext in ['.doc', '.docx']):
            raise ValidationError("Word document type requires a .doc or .docx file")

        if self.document_type == 'gdoc' and not self.google_doc_id:
            raise ValidationError("Google Docs require a document ID")

    def __str__(self):
        return f"{self.title} ({self.get_document_type_display()})"