from edge_system import app #, socketio



#Load configuration
#app.config.from_object('configuration.DevelopmentConfig')
#app.config.from_object('configuration.BaseConfig')

print(app.url_map)

#app.run()
app.run(host='0.0.0.0', port=5055)

#socketio.run(app, host='0.0.0.0', port=5055)