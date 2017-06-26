The main disadvantage of the Kivy framework I encountered is that it is mainly centered on the ability to enhance Python applications' capabilities on different devices, leaving matters of app building convenience behind.

Fortunately, it is not complicated to create tools that add some abstraction for game building. The aim is to create a framework that allows an enthusiast to skip all the programming routine and concentrate on the fun part, game designing.

Functionality by now:
#### Graphics
* Scanning directories for YAML scripts
* Loading images and atlas files based on YAML scripts
* Providing paths to them using locale settings with fallback to default locale
* Display an empty image if id not found

#### Audio
* Scanning directories for YAML scripts
* Loading audio files based on YAML scripts using locale settings
* Playing music (sound in loop with only on file at time) by id
* Playing sound effects by id

#### Text
* Scanning directories for YAML scripts
* Templates based on Jinja2
* Providing text strings by id using locale settings
* String id displayed if id not found

#### Configuration
Built on own YAML configuration files

* Scanning directories for YAML scripts
* Loading, saving and initializing user config

#### Scripting
* Scanning directories for Kv scripts