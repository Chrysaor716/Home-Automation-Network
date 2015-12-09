# Home-Automation-Network
Integration of four Raspberry Pi's to create an interactive home environment.

The Pi's interact on a local network with either RabbitMQ as the message broker or sockets. One Pi act as a central server, with the rest communicating via that single server.

	Pi 1: User Interaction
Takes in voice input or a web-based input from the user.

	Pi 2: Server
Central server that processes data and acts as the bridge between all the Pi's.

	Pi 3: Sensors for surrounding data
For this project, it uses a temperature sensor and takes the average temperature over an arbitrary period of time.

	Pi 4: Controllable devices
An LED in place of a lamp or other light source is used for the purpose of demonstrating the project.
