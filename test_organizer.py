import os
import shutil
import unittest
from file_organizer import FileOrganizer


class TestFileOrganizer(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.abspath("temp_unit_test_folder")
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir, exist_ok=True)
        self.organizer = FileOrganizer(self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def create_file(self, filename, content="dummy"):
        path = os.path.join(self.test_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_category_detection(self):
        self.assertEqual(self.organizer.get_category("photo.jpg"), "Images")
        self.assertEqual(self.organizer.get_category("diagram.PNG"), "Images")
        self.assertEqual(self.organizer.get_category("art.jpeg"), "Images")
        self.assertEqual(self.organizer.get_category("doc.pdf"), "Documents")
        self.assertEqual(self.organizer.get_category("file.docx"), "Documents")
        self.assertEqual(self.organizer.get_category("notes.txt"), "Documents")
        self.assertEqual(self.organizer.get_category("movie.mp4"), "Videos")
        self.assertEqual(self.organizer.get_category("clip.mkv"), "Videos")
        self.assertEqual(self.organizer.get_category("script.py"), "Python Files")
        self.assertEqual(self.organizer.get_category("archive.zip"), "Others")
        self.assertEqual(self.organizer.get_category("data.csv"), "Others")
        self.assertEqual(self.organizer.get_category("unknown"), "Others")

    def test_preview_mode_does_not_move_files(self):
        self.create_file("test.pdf")
        self.create_file("photo.jpg")

        results = self.organizer.organize(preview=True)
        self.assertEqual(len(results), 2)

        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "test.pdf")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "photo.jpg")))
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "Documents", "test.pdf")))
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "Images", "photo.jpg")))

    def test_organize_moves_files(self):
        self.create_file("test.pdf")
        self.create_file("photo.jpg")
        self.create_file("script.py")
        self.create_file("video.mp4")
        self.create_file("archive.rar")

        results = self.organizer.organize(preview=False)
        self.assertEqual(len(results), 5)

        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Documents", "test.pdf")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Images", "photo.jpg")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Python Files", "script.py")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Videos", "video.mp4")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Others", "archive.rar")))

        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "test.pdf")))

    def test_duplicate_handling(self):
        images_dir = os.path.join(self.test_dir, "Images")
        os.makedirs(images_dir, exist_ok=True)
        with open(os.path.join(images_dir, "pic.png"), "w") as f:
            f.write("existing")

        self.create_file("pic.png", "new file")

        self.organizer.organize(preview=False)

        self.assertTrue(os.path.exists(os.path.join(images_dir, "pic.png")))
        self.assertTrue(os.path.exists(os.path.join(images_dir, "pic_1.png")))

        with open(os.path.join(images_dir, "pic.png"), "r") as f:
            self.assertEqual(f.read(), "existing")
        with open(os.path.join(images_dir, "pic_1.png"), "r") as f:
            self.assertEqual(f.read(), "new file")

    def test_log_file_creation(self):
        self.create_file("document.txt")
        self.organizer.organize(preview=False)

        log_path = self.organizer.log_path
        self.assertTrue(os.path.exists(log_path))

        with open(log_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("document.txt", content)
            self.assertIn("Documents", content)


if __name__ == "__main__":
    unittest.main()
