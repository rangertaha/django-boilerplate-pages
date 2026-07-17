"""Tests for the ``pages`` app: models, signals, URLs, views and admin."""

from django.contrib import admin as django_admin
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .admin import PageAdmin, SectionAdmin
from .models import Page, Section


class PageModelTests(TestCase):
    def test_str_returns_slug(self):
        page = Page.objects.create(title="About Us", order=1)
        self.assertEqual(str(page), "about-us")

    def test_slug_generated_from_title(self):
        page = Page.objects.create(title="Hello World", order=1)
        self.assertEqual(page.slug, "hello-world")

    def test_explicit_slug_is_preserved(self):
        page = Page.objects.create(title="Hello World", slug="custom", order=1)
        self.assertEqual(page.slug, "custom")

    def test_defaults(self):
        page = Page.objects.create(title="Defaults", order=1)
        self.assertTrue(page.active)
        self.assertEqual(page.status, 0)  # Draft
        self.assertIsNotNone(page.created)
        self.assertIsNotNone(page.updated)

    def test_timestamp_field_semantics(self):
        """created is set once on creation; updated refreshes on every save."""
        created_field = Page._meta.get_field("created")
        updated_field = Page._meta.get_field("updated")
        self.assertTrue(created_field.auto_now_add)
        self.assertFalse(created_field.auto_now)
        self.assertTrue(updated_field.auto_now)
        self.assertFalse(updated_field.auto_now_add)

    def test_created_fixed_and_updated_advances_on_save(self):
        page = Page.objects.create(title="Stamps", order=1)
        original_created = page.created
        original_updated = page.updated
        page.title = "Stamps edited"
        page.save()
        page.refresh_from_db()
        self.assertEqual(page.created, original_created)
        self.assertGreater(page.updated, original_updated)

    def test_ordering_by_order_field(self):
        Page.objects.create(title="Second", order=2)
        Page.objects.create(title="First", order=1)
        Page.objects.create(title="Third", order=3)
        self.assertEqual(
            list(Page.objects.values_list("slug", flat=True)),
            ["first", "second", "third"],
        )

    def test_tree_parent_child_relationship(self):
        root = Page.objects.create(title="Root", order=1)
        child = Page.objects.create(title="Child", order=1, parent=root)
        root.refresh_from_db()
        child.refresh_from_db()
        self.assertIn(child, root.children.all())
        self.assertEqual(child.parent, root)
        self.assertEqual(child.get_level(), 1)
        self.assertTrue(child.is_leaf_node())
        self.assertFalse(root.is_leaf_node())

    def test_tree_descendants_and_ancestors(self):
        root = Page.objects.create(title="P Root", order=1)
        child = Page.objects.create(title="P Child", order=1, parent=root)
        grandchild = Page.objects.create(title="P Grand", order=1, parent=child)
        root.refresh_from_db()
        grandchild.refresh_from_db()
        self.assertEqual(
            list(root.get_descendants().values_list("slug", flat=True)),
            ["p-child", "p-grand"],
        )
        self.assertEqual(
            list(grandchild.get_ancestors().values_list("slug", flat=True)),
            ["p-root", "p-child"],
        )

    def test_tree_rebuilt_after_save(self):
        """Page.save() rebuilds the MPTT tree, keeping lft/rght consistent."""
        root = Page.objects.create(title="R", order=1)
        a = Page.objects.create(title="A", order=2, parent=root)
        b = Page.objects.create(title="B", order=1, parent=root)
        root.refresh_from_db()
        a.refresh_from_db()
        b.refresh_from_db()
        self.assertEqual(root.lft, 1)
        self.assertEqual(root.rght, 6)
        # order_insertion_by=['order'] places B (order=1) before A (order=2).
        self.assertLess(b.lft, a.lft)

    def test_siblings_ordered_by_order_insertion(self):
        root = Page.objects.create(title="Top", order=1)
        Page.objects.create(title="Zeta", order=1, parent=root)
        Page.objects.create(title="Alpha", order=2, parent=root)
        root.refresh_from_db()
        self.assertEqual(
            list(root.get_children().values_list("slug", flat=True)),
            ["zeta", "alpha"],
        )


class SectionModelTests(TestCase):
    def test_str_returns_slug(self):
        section = Section.objects.create(name="Getting Started", order=1)
        self.assertEqual(str(section), "getting-started")

    def test_slug_generated_from_name(self):
        section = Section.objects.create(name="My Section", order=1)
        self.assertEqual(section.slug, "my-section")

    def test_explicit_slug_is_preserved(self):
        section = Section.objects.create(name="My Section", slug="other", order=1)
        self.assertEqual(section.slug, "other")

    def test_defaults(self):
        section = Section.objects.create(name="Defaults", order=1)
        self.assertTrue(section.active)
        self.assertTrue(section.public)

    def test_timestamp_field_semantics(self):
        """created is set once on creation; updated refreshes on every save."""
        created_field = Section._meta.get_field("created")
        updated_field = Section._meta.get_field("updated")
        self.assertTrue(created_field.auto_now_add)
        self.assertFalse(created_field.auto_now)
        self.assertTrue(updated_field.auto_now)
        self.assertFalse(updated_field.auto_now_add)

    def test_ordering_by_order_field(self):
        Section.objects.create(name="B", order=2)
        Section.objects.create(name="A", order=1)
        self.assertEqual(
            list(Section.objects.values_list("slug", flat=True)),
            ["a", "b"],
        )

    def test_tree_parent_child_relationship(self):
        root = Section.objects.create(name="Root", order=1)
        child = Section.objects.create(name="Child", order=1, parent=root)
        root.refresh_from_db()
        self.assertIn(child, root.children.all())
        self.assertEqual(list(root.get_descendants()), [child])

    def test_pages_many_to_many(self):
        section = Section.objects.create(name="Docs", order=1)
        page = Page.objects.create(title="Intro", order=1)
        section.pages.add(page)
        self.assertIn(page, section.pages.all())
        self.assertIn(section, page.section_set.all())

    def test_pages_limited_to_active_choices(self):
        field = Section._meta.get_field("pages")
        self.assertEqual(field.remote_field.limit_choices_to, {"active": True})


class UrlTests(TestCase):
    def test_reverse_index(self):
        self.assertEqual(reverse("index"), "/")

    def test_reverse_section(self):
        self.assertEqual(reverse("section", args=["docs"]), "/docs")

    def test_reverse_top_page(self):
        self.assertEqual(reverse("top-page", args=["docs", "intro"]), "/docs/intro")

    def test_reverse_child_page(self):
        self.assertEqual(
            reverse("child-page", args=["docs", "intro", "setup"]),
            "/docs/intro/setup",
        )


class IndexViewTests(TestCase):
    def test_index_renders(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/index.html")


class SectionViewTests(TestCase):
    def setUp(self):
        self.section = Section.objects.create(name="Docs", order=1)
        self.page = Page.objects.create(title="Intro", order=1)
        self.section.pages.add(self.page)

    def test_active_root_section_renders(self):
        response = self.client.get(reverse("section", args=["docs"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/index.html")
        self.assertEqual(response.context["section"], self.section)

    def test_navbar_mixin_provides_sections(self):
        response = self.client.get(reverse("section", args=["docs"]))
        self.assertIn(self.section, response.context["sections"])

    def test_inactive_section_returns_404(self):
        Section.objects.create(name="Hidden", order=2, active=False)
        response = self.client.get(reverse("section", args=["hidden"]))
        self.assertEqual(response.status_code, 404)

    def test_child_section_returns_404(self):
        Section.objects.create(name="Child", order=1, parent=self.section)
        response = self.client.get(reverse("section", args=["child"]))
        self.assertEqual(response.status_code, 404)

    def test_unknown_section_returns_404(self):
        response = self.client.get(reverse("section", args=["missing"]))
        self.assertEqual(response.status_code, 404)


class PageViewTests(TestCase):
    def setUp(self):
        self.section = Section.objects.create(name="Docs", order=1)
        self.page = Page.objects.create(title="Intro", order=1)
        self.section.pages.add(self.page)

    def test_active_page_renders(self):
        response = self.client.get(reverse("top-page", args=["docs", "intro"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/index.html")
        self.assertEqual(response.context["page"], self.page)

    def test_menu_mixin_provides_section(self):
        response = self.client.get(reverse("top-page", args=["docs", "intro"]))
        self.assertEqual(response.context["section"], self.section)

    def test_inactive_page_returns_404(self):
        Page.objects.create(title="Secret", order=2, active=False)
        response = self.client.get(reverse("top-page", args=["docs", "secret"]))
        self.assertEqual(response.status_code, 404)

    def test_child_page_url_renders(self):
        child = Page.objects.create(title="Setup", order=1, parent=self.page)
        response = self.client.get(
            reverse("child-page", args=["docs", "intro", "setup"])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page"], child)


class AdminTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="password"
        )
        self.client.force_login(self.user)

    def test_models_registered(self):
        self.assertIsInstance(django_admin.site._registry[Page], PageAdmin)
        self.assertIsInstance(django_admin.site._registry[Section], SectionAdmin)

    def test_page_changelist_renders(self):
        Page.objects.create(title="Intro", order=1)
        response = self.client.get(reverse("admin:pages_page_changelist"))
        self.assertEqual(response.status_code, 200)

    def test_section_changelist_renders(self):
        Section.objects.create(name="Docs", order=1)
        response = self.client.get(reverse("admin:pages_section_changelist"))
        self.assertEqual(response.status_code, 200)

    def test_page_changelist_search(self):
        match = Page.objects.create(title="Search Target", order=1)
        Page.objects.create(title="Other", order=2)
        response = self.client.get(
            reverse("admin:pages_page_changelist"), {"q": "target"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["cl"].queryset), [match])

    def test_page_search_fields_are_text_fields(self):
        for name in PageAdmin.search_fields:
            field = Page._meta.get_field(name)
            self.assertIn(
                field.get_internal_type(),
                ("CharField", "SlugField", "TextField"),
                f"search field {name!r} is not a text field",
            )

    def test_section_changelist_search(self):
        match = Section.objects.create(name="Docs Portal", order=1)
        Section.objects.create(name="Other", order=2)
        response = self.client.get(
            reverse("admin:pages_section_changelist"), {"q": "portal"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["cl"].queryset), [match])

    def test_page_add_form_renders(self):
        response = self.client.get(reverse("admin:pages_page_add"))
        self.assertEqual(response.status_code, 200)

    def test_section_add_form_renders(self):
        response = self.client.get(reverse("admin:pages_section_add"))
        self.assertEqual(response.status_code, 200)
