import virtualbox, asyncio
#This is not a cog and should not be imported as a cog!!

#Get a screenshot of a VM using a Session object.
def get_vm_screenshot(vm_sesh, file_name):
    h, w, _, _, _, _ = vm_sesh.console.display.get_screen_resolution(0)
    png = vm_sesh.console.display.take_screen_shot_to_array(0, h, w, virtualbox.library.BitmapFormat.png)
    with open(file_name, 'wb') as file:
        file.write(png)



if __name__ == "__main__":
    print("This is a library or cog and should not be executed directly.")