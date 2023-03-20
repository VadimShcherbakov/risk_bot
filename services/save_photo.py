
async def get_photo(message):
    file_info = await bot.get_file(message.photo[-1].file_id)
    print(file_info)
    print(file_info.file_path.split('photos/')[1])
    await bot.download(file_info,file_info.file_path.split('photos/')[1])
