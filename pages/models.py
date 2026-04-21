from django.db import models


PRODUCT_CHOICES = [
    ("buksa", "Buksa"),
    ("hotgoss", "HotGoss"),
    ("samesky", "SameSky"),
    ("taskmatic", "Taskmatic"),
]


class Conversion(models.Model):
    product = models.CharField(max_length=20, choices=PRODUCT_CHOICES, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)
    session_id = models.CharField(max_length=64, blank=True)
    ip_hash = models.CharField(max_length=64, blank=True)
    button_label = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = "ads_set_v1_pages_conversion"
        indexes = [
            models.Index(fields=["product", "timestamp"]),
        ]

    def __str__(self):
        return f"{self.product} — {self.button_label} @ {self.timestamp:%Y-%m-%d %H:%M}"
