#!/usr/bin/env python3
"""
Global ASB Session Project Navigation Regression Tests
Tests: PROJECT_REGISTRY integrity, session schema, migration idempotency,
       link resolution, Workdesk chain, daily project link.
"""
import os, re, csv, unittest

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
REGISTRY_PATH = os.path.join(repo_root, "projects/PROJECT_REGISTRY.tsv")

def load_registry():
    rows = []
    with open(REGISTRY_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            rows.append(row)
    return rows

def get_session_files():
    sessions_root = os.path.join(repo_root, "worklog/sessions")
    files = []
    for root, _, fnames in os.walk(sessions_root):
        for fn in fnames:
            if fn.endswith(".md"):
                files.append(os.path.join(root, fn))
    return sorted(files)

def parse_frontmatter(content):
    m = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not m:
        return None
    return m.group(1)

class TestProjectRegistryIntegrity(unittest.TestCase):
    """Test 1: PROJECT_REGISTRY_INTEGRITY"""

    def test_registry_exists(self):
        self.assertTrue(os.path.exists(REGISTRY_PATH), "PROJECT_REGISTRY.tsv is missing")

    def test_project_ids_unique(self):
        rows = load_registry()
        ids = [r["project_id"] for r in rows]
        self.assertEqual(len(ids), len(set(ids)), "Duplicate project_ids in registry")

    def test_project_paths_exist_if_canonical(self):
        rows = load_registry()
        for row in rows:
            pp = row["project_path"]
            if not pp:
                continue
            full = os.path.join(repo_root, pp)
            # Only fail if the path is claimed but not present for known-canonical projects
            if row["project_id"] in ("AIRO_WORKDESK", "AIRO_SECOND_BRAIN", "EARESMES_ARFIN_CLARIFICATION_BRIDGE"):
                self.assertTrue(os.path.exists(full),
                    f"Registry project_path missing for {row['project_id']}: {pp}")

    def test_knowledge_paths_exist_if_specified(self):
        rows = load_registry()
        for row in rows:
            kp = row["knowledge_path"]
            if not kp:
                continue
            full = os.path.join(repo_root, kp)
            self.assertTrue(os.path.exists(full),
                f"Registry knowledge_path missing for {row['project_id']}: {kp}")

    def test_workdesk_in_registry(self):
        rows = load_registry()
        ids = [r["project_id"] for r in rows]
        self.assertIn("AIRO_WORKDESK", ids, "AIRO_WORKDESK not in registry")

    def test_asb_in_registry(self):
        rows = load_registry()
        ids = [r["project_id"] for r in rows]
        self.assertIn("AIRO_SECOND_BRAIN", ids, "AIRO_SECOND_BRAIN not in registry")


class TestSessionProjectSchema(unittest.TestCase):
    """Tests 2-7: session schema, link resolution, preservation"""

    def test_all_airo_sessions_have_project_id(self):
        for fp in get_session_files():
            content = open(fp, encoding="utf-8").read()
            fm = parse_frontmatter(content)
            if fm and "type: airo-session" in fm:
                self.assertIn("project_id:", fm,
                    f"Missing project_id in {os.path.basename(fp)}")

    def test_all_airo_sessions_have_project_name(self):
        for fp in get_session_files():
            content = open(fp, encoding="utf-8").read()
            fm = parse_frontmatter(content)
            if fm and "type: airo-session" in fm:
                self.assertIn("project_name:", fm,
                    f"Missing project_name in {os.path.basename(fp)}")

    def test_all_airo_sessions_have_clickable_project(self):
        for fp in get_session_files():
            content = open(fp, encoding="utf-8").read()
            fm = parse_frontmatter(content)
            if fm and "type: airo-session" in fm:
                proj_line = re.search(r'^project:\s*"?(.*?)"?\s*$', fm, re.MULTILINE)
                self.assertIsNotNone(proj_line, f"No project: field in {os.path.basename(fp)}")
                self.assertIn("[[", proj_line.group(1),
                    f"project: field not clickable wikilink in {os.path.basename(fp)}")

    def test_all_project_wikilinks_resolve(self):
        """Test 5: PROJECT_LINK_RESOLUTION"""
        for fp in get_session_files():
            content = open(fp, encoding="utf-8").read()
            fm = parse_frontmatter(content)
            if not fm or "type: airo-session" not in fm:
                continue
            proj_match = re.search(r'\[\[(projects/[^\|]+)\|', fm)
            if proj_match:
                link_target = proj_match.group(1) + ".md"
                full = os.path.join(repo_root, link_target)
                self.assertTrue(os.path.exists(full),
                    f"project wikilink target missing: {link_target} in {os.path.basename(fp)}")

    def test_all_knowledge_wikilinks_resolve(self):
        """Test 6: KNOWLEDGE_LINK_RESOLUTION"""
        for fp in get_session_files():
            content = open(fp, encoding="utf-8").read()
            fm = parse_frontmatter(content)
            if not fm or "type: airo-session" not in fm:
                continue
            know_match = re.search(r'^knowledge:\s*"?\[\[(.*?)\|', fm, re.MULTILINE)
            if know_match:
                link_target = know_match.group(1) + ".md"
                full = os.path.join(repo_root, link_target)
                self.assertTrue(os.path.exists(full),
                    f"knowledge wikilink target missing: {link_target}")

    def test_semantic_preservation(self):
        """Test 4: HISTORICAL_SEMANTIC_PRESERVATION"""
        for fp in get_session_files():
            content = open(fp, encoding="utf-8").read()
            fm = parse_frontmatter(content)
            if not fm or "type: airo-session" not in fm:
                continue
            for field in ["objective:", "status:", "can_advance:"]:
                if field in fm:
                    m = re.search(f'^{field}.*', fm, re.MULTILINE)
                    self.assertIsNotNone(m, f"{field} missing after migration in {os.path.basename(fp)}")

    def test_migration_idempotency(self):
        """Test 10: MIGRATION_IDEMPOTENCY — no unmigrated eligible sessions"""
        unmigrated = []
        for fp in get_session_files():
            content = open(fp, encoding="utf-8").read()
            fm = parse_frontmatter(content)
            if fm and "type: airo-session" in fm:
                if "project_id:" not in fm or '[[' not in fm:
                    unmigrated.append(os.path.basename(fp))
        self.assertEqual(len(unmigrated), 0,
            f"Sessions not yet migrated: {unmigrated}")


class TestWorkDeskNavigationChain(unittest.TestCase):
    """Test 12: WORKDESK_PATH chain Session->Project->Wiki"""

    def test_workdesk_session_project_link(self):
        wd_sessions = [fp for fp in get_session_files()
                       if "AIRO WorkDesk" in fp or "airo-workdesk" in fp.lower()]
        self.assertGreater(len(wd_sessions), 0, "No AIRO WorkDesk session files found")
        for fp in wd_sessions:
            content = open(fp, encoding="utf-8").read()
            fm = parse_frontmatter(content)
            self.assertIn("AIRO_WORKDESK", fm,
                f"AIRO WorkDesk session missing project_id: {os.path.basename(fp)}")
            self.assertIn("projects/airo-workdesk", fm,
                f"AIRO WorkDesk session missing project wikilink: {os.path.basename(fp)}")

    def test_workdesk_project_file_links_to_knowledge(self):
        proj_path = os.path.join(repo_root, "projects/airo-workdesk.md")
        self.assertTrue(os.path.exists(proj_path))
        content = open(proj_path, encoding="utf-8").read()
        self.assertIn("wiki/workdesk/HOME", content,
            "projects/airo-workdesk.md does not link to wiki/workdesk/HOME")

    def test_workdesk_knowledge_home_exists(self):
        self.assertTrue(os.path.exists(os.path.join(repo_root, "wiki/workdesk/HOME.md")))

    def test_workdesk_session_knowledge_link(self):
        wd_sessions = [fp for fp in get_session_files()
                       if "AIRO WorkDesk" in fp]
        for fp in wd_sessions:
            content = open(fp, encoding="utf-8").read()
            fm = parse_frontmatter(content)
            if fm and "project_id: AIRO_WORKDESK" in fm:
                self.assertIn("wiki/workdesk/HOME", fm,
                    f"AIRO WorkDesk session missing knowledge link: {os.path.basename(fp)}")


class TestDailyProjectLink(unittest.TestCase):
    """Test 9: DAILY_PROJECT_LINK"""

    def test_airo_daily_has_resolver(self):
        daily_path = os.path.join(repo_root, "scripts/airo-daily")
        content = open(daily_path, encoding="utf-8").read()
        self.assertIn("_resolve_project_for_daily", content,
            "airo-daily does not have project resolver function")

    def test_airo_daily_uses_registry(self):
        daily_path = os.path.join(repo_root, "scripts/airo-daily")
        content = open(daily_path, encoding="utf-8").read()
        self.assertIn("PROJECT_REGISTRY.tsv", content,
            "airo-daily does not reference PROJECT_REGISTRY.tsv")


class TestProjectIndex(unittest.TestCase):
    """Test: projects/_index.md and CONTEXT.md pointer"""

    def test_project_index_exists(self):
        self.assertTrue(os.path.exists(os.path.join(repo_root, "projects/_index.md")),
            "projects/_index.md is missing (CONTEXT.md references it)")

    def test_project_index_references_workdesk(self):
        content = open(os.path.join(repo_root, "projects/_index.md"), encoding="utf-8").read()
        self.assertIn("airo-workdesk", content)

    def test_airo_second_brain_project_file_exists(self):
        self.assertTrue(os.path.exists(os.path.join(repo_root, "projects/airo-second-brain.md")))


if __name__ == "__main__":
    unittest.main()
