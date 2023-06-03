import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from compression import compress_to_zip
from validate_path import validate_linux_path

class MainWindow:
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("GUI/GUI.glade")

        self.window = builder.get_object("main_window")
        self.window.set_title("TurboZipCompressor")

        self.button = builder.get_object("button_chooseFile")
        self.radio_button_same_path = builder.get_object("same_path")
        self.radio_button_custom_path = builder.get_object("custom_path")
        self.insert_path_entry = builder.get_object("insert_path_entry")
        
        self.menu_bar = builder.get_object("menu_bar")
        self.menu_item_about = Gtk.MenuItem(label="About")
        self.menu_item_about.connect("activate", self.on_about_clicked)
        self.menu_bar.append(self.menu_item_about)

        self.menu_item_help = Gtk.MenuItem(label="Help")
        self.menu_item_help.connect("activate", self.on_help_clicked)
        self.menu_bar.append(self.menu_item_help)

        self.button.connect("clicked", self.on_button_chooseFile_clicked)
        self.radio_button_same_path.connect("toggled", self.on_radio_button_toggled)
        self.radio_button_custom_path.connect("toggled", self.on_radio_button_toggled)
        self.window.connect("destroy", Gtk.main_quit)
        

    def on_button_chooseFile_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Wybierz plik",
            parent=self.window,
            action=Gtk.FileChooserAction.OPEN,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK,
        )

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            print("Choosen file:", filename)

            if self.radio_button_same_path.get_active():
                compressed_file_path = os.path.splitext(filename)[0] + ".zip"
            elif self.radio_button_custom_path.get_active():
                custom_path = self.insert_path_entry.get_text()
                if validate_linux_path(custom_path):
                    compressed_file_path = os.path.join(custom_path, os.path.basename(filename))
                    compressed_file_path = os.path.splitext(compressed_file_path)[0] + ".zip"
                else:
                    print("Invalid path:", custom_path)
                    dialog.destroy()
                    return
                    
            if compressed_file_path != filename:
                compress_to_zip(filename, compressed_file_path)
                print("Compressed file saved at:", compressed_file_path)
                self.show_message_dialog("Success", "File compressed successfully!")
            else:
                compressed_file_path = os.path.splitext(filename)[0] + "_compressed.zip"
                compress_to_zip(filename, compressed_file_path)
                print("Compressed file saved at:", compressed_file_path)
                self.show_message_dialog("Success", "File compressed successfully!")

        dialog.destroy()

    def show_message_dialog(self, title, message):
        dialog = Gtk.MessageDialog(
            parent=self.window,
            flags=0,
            type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            message_format=message,
        )
        dialog.set_title(title)
        dialog.run()
        dialog.destroy()

    def on_about_clicked(self, widget):
        about_dialog = Gtk.AboutDialog()
        about_dialog.set_program_name("TurboZipCompressor")
        about_dialog.set_version("1.0")
        about_dialog.set_authors(["@Walu064 https://github.com/Walu064 :)"])
        about_dialog.run()
        about_dialog.destroy()    

    def on_help_clicked(self, widget):
        help_dialog = Gtk.MessageDialog(
            parent=self.window,
            flags=Gtk.DialogFlags.MODAL,
            type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            message_format="User Manual:\n\n"
                          "1. Choose the save option (same path or custom path).\n"
                          "2. Click the \"choose file to compress\" button.\n"
                          "3. Choose file, click \"Open\". Done!"
        )
        help_dialog.run()
        help_dialog.destroy()

    def on_radio_button_toggled(self, widget):
        if self.radio_button_same_path.get_active():
            self.insert_path_entry.set_sensitive(False)
        elif self.radio_button_custom_path.get_active():
            self.insert_path_entry.set_sensitive(True)

    def run(self):
        self.window.show_all()
        Gtk.main()

if __name__ == "__main__":
    app = MainWindow()
    app.run()