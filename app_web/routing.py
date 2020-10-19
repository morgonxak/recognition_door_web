from app_web import app
from flask import request, render_template, make_response, url_for
import pickle
import os
from werkzeug.utils import secure_filename
import uuid
import json
import shutil
from app_web.moduls.trening_models_cvm_knn import get_encodings_and_personId_by_image, train_cvm, train_knn, save_model, save_BD_signs
from app_web.moduls import trening_models_cvm_knn

@app.route('/addUser/', methods=['GET', 'POST'])
def add_user_web():
    '''
    Вызывает окно и добовляет фотографии позьзователя в систему
    :return:
    '''
    if request.method == 'POST':
        person_id = str(uuid.uuid4())
        last_name = request.form.get("last_name")
        first_name = request.form.get("first_name")
        middle_name = request.form.get("middle_name")
        mode_skip = request.form.get("mode_skip")
        photos = request.files.getlist("photos")

        if add_photo(photos, person_id):
            status_photo = 1
        else:
            status_photo = 0

        if app.config['database'].add_user(last_name, first_name, middle_name, mode_skip, status_photo, person_id) != -1:
            return go_index("Пользователь успешно добавлен")
        #
        else:
            return go_index("Что-то пошло не так")
    else:
        return render_template('add_webUser.html', URL=app.config['IP_Server'] + ':' + str(app.config['PORT_server']))

def add_photo(photos, personId):
    def create_dir(path_dir):
        if not os.path.isdir(path_dir):
            os.mkdir(path_dir)

    Flag = False
    # Фото для тренировки сети
    for count, photo_trener in enumerate(photos):
        filename = secure_filename(photo_trener.filename)
        if filename[filename.rfind('.'):] != '':
            Flag = True
            create_dir(os.path.join(app.config['TEMP'], personId))
            create_dir(os.path.join(app.config['TEMP'], personId, 'RGB'))
            photo_trener.save(os.path.join(app.config['TEMP'], personId, 'RGB', str(count) + filename[filename.rfind('.'):]))
    return Flag

def go_index(text):
    list_users = app.config['database'].get_users()
    return render_template('index.html', rows=list_users, text=text)

@app.route('/update/<personId>', methods=['GET', 'POST'])
def updateUser(personId):

    if request.method == 'POST':
        last_name = request.form.get("last_name")
        first_name = request.form.get("first_name")
        middle_name = request.form.get("middle_name")
        mode_skip = request.form.get("mode_skip")

        photos = request.files.getlist("photos")
        print(photos)
        print(type(photos[0]))
        status_photo = None
        if add_photo(photos, personId):
            status_photo = 1

        if app.config['database'].update_user_by_personId(personId, last_name, first_name, middle_name, mode_skip) != -1:
            if not status_photo is None:
                app.config['database'].update_status_photo_by_personId(personId, status_photo)

            return go_index('Данные успешно обновлены')
        else:
            return go_index('Что-то пошло не так')

    else:
        user = app.config['database'].getInformation_by_personID(personId)
        return render_template('update.html', user=user)

@app.route('/update/<personId>/deluser/', methods=['GET', 'POST'])
def del_user(personId):
    print(personId)
    if app.config['database'].del_user(personId) != -1:
        return go_index("Пользователь удален")
    else:
        return go_index("Что-то пошло нет так")

@app.route('/classification', methods=['GET', 'POST'])
def classification():
    '''
    Обучить классификатор
    :return:
    '''
    list_user_temp = os.listdir(app.config['TEMP'])
    for personID in list_user_temp:
        if app.config['database'].getInformation_by_personID(personID) != -1:
            path_photo = os.path.join(app.config['TEMP'], personID, 'RGB')
            list_classificotors = []
            for photo in os.listdir(path_photo):
                list_classificotors.append(list(get_encodings_and_personId_by_image(os.path.join(path_photo, photo))))

            if len(list_classificotors) != 0:
                app.config['database'].pull_descriptors(personID, json.dumps(list_classificotors))

        print(os.path.join(app.config['TEMP'], personID))
        # os.rmdir(os.path.join(app.config['TEMP'], personID))

        shutil.rmtree(os.path.join(app.config['TEMP'], personID))

    print("Все данные добавленны, начинаем обучение")
    person_id, encodings = app.config['database'].get_descriptors()

    trening_models_cvm_knn.encodings = encodings
    trening_models_cvm_knn.person_id = person_id
    try:

        if len(set(trening_models_cvm_knn.person_id)) >= 2:
            print('обучаем нейросети')
            clf_svm = train_cvm()
            clf_knn = train_knn()
            print("обучение завершено")
            save_BD_signs(os.path.join(app.config['PATH_SAVE_MODEL'], 'dataBase_1.pk'))
        else:
            return go_index(str("Количество пользователей менее 2 человек"))
    except BaseException as e:
        print("Error {}".format(e))
        return go_index(str("Что-то пошло не так"))
    # pref = str(1)
    # save_model(clf_svm, os.path.join(app.config['RC'], "svm_model_" + pref + '.pk'))
    # save_model(clf_knn, os.path.join(app.config['RC'], "knn_model_" + pref + '.pk'))

    return go_index(str("Обучение завершено"))

@app.route('/')
def index(text=''):
    #free = 100
    list_mode = []
    updateList = []
    list_users = app.config['database'].get_users()
    # listTemp = os.listdir(app.config['TEMP'])
    # for user in list_users:
    #     personId = user[0]
    #     last_name = user[1]
    #     first_name = user[2]
    #     middle_name = user[3]
    #     mode_skip = user[4]
    #     del_user = user[5]
    #     status_photo = user[6]
    #     #print(personId, last_name, first_name, middle_name, mode_skip, status_photo)
    #     if personId is listTemp:
    #         photoDB = str(0)
    #     else:
    #         photoDB = str("adsa")
    #
    #     updateList.append(tuple([personId, last_name, first_name, middle_name, mode_skip, status_photo, del_user, photoDB]))

        # list_mode.append(user + personId)

    return render_template('index.html', rows=list_users, text=text,  URL='http://' + app.config['IP_Server'] + ':' + str(app.config['PORT_server']))