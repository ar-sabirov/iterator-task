Функционал для итерации по данным из источников rgb, depth, touch

src/dataset.py - Базовый итератор, который делает ресемплинг на количество семплов и частоту в данных touch    
src/indicies.py - построение индексов для выравненной по времени итерации по данным    
src/async_dataset.py - Асинхронная надстройка над базовым итератором    
src/util.oy - вспомогательные функции для чтения данных из источников    

tests/test_indicies.py - тест для функции get_indicies, хорошо иллюстрирует результат работы выравнивания

run.py - cli для тестового запуста

pip install -r requirements.txt

Синхронно:
python run.py -p /path/to/dataset/root/

Асинхронно:
python run.py -d True -p /path/to/dataset/root/
