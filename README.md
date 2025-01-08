# Sahana Eden

Sahana Eden is an Emergency Development Environment—an open-source platform designed to help Disaster Management practitioners mitigate, prepare for, respond to, and recover from disasters. It supports a wide range of activities, including managing organizations, people, projects, inventory, and assets, providing situational awareness through maps, and facilitating communication.

## Key Features
- **Organization Registry**: Tracks active organizations, offices, and field sites.
- **Project Tracking**: Monitors disaster management projects and collaborations.
- **Human Resources Management**: Manages volunteers, staff, and their skills.
- **Inventory Management**: Tracks essential supplies and automates logistics.
- **Asset Management**: Keeps records of vehicles, equipment, and other resources.
- **Assessments**: Collects and analyzes data for disaster planning and response.
- **Mapping**: Provides visual data for situational awareness using GIS tools.
- **Shelter Management**: Tracks shelter details and population demographics.
- **Messaging System**: Supports communication via SMS, email, and social platforms.

## Who Uses Sahana Eden?
Sahana Eden is used by organizations worldwide, including:
- Humanitarian NGOs (e.g., HELIOS Foundation, Red Cross).
- Disaster risk reduction platforms (e.g., DRR Project Portal).
- Emergency response teams during disasters (e.g., Haiti 2010 Earthquake).

## Installation
Sahana Eden can run on Linux, Windows, or MacOS. The recommended environment is Debian Linux with Python, Web2py, and a supported database (MySQL, PostgreSQL, SQLite).

Installation scripts and detailed instructions are available on the Wiki:

http://eden.sahanafoundation.org/wiki/InstallationGuidelines

Note that the first user to register gets administrator privileges for the system.

If you need to customize the code, it is recommended to set up a release process. Ideally, this would include a separate development instance and a User Acceptance Testing (UAT) instance, which can be run on the same server.

Directory Structure
After the installation, the typical directory structure of the instance looks like:

[FileSystemLayout](FileSystemLayout.png)

Troubleshooting Installation
Initial installation issues are generally due to missed installation steps or a non-standard site configuration. Typical issues are:

Obsolete release packages:
The latest functionality will not be available in packaged releases which are available for download. Currently we advise users to install the latest development version from source instead.

Folder names:
Web2Py does not support hyphens in the application folder name. If you specify a target folder name when cloning, be sure to specify a target folder name without a hyphen in.

Linux permissions:
Web2py needs to be able to write in several Sahana Eden directories: cache, databases, errors, sessions, and uploads. The installation instructions and scripts should set the correct permissions. If you encounter permission errors, refer to the installation instructions and run the commands that set permissions and ownership of the Eden directories. 

Apache configuration:
Apache with mod_wsgi does not support underscores in hostnames. (Underscores are not a legal hostname character according to the formal W3 URI specification.)

If there are multiple mod_wsgi sites enabled, each must have its own WSGIDaemonProcess name.

It is possible to run multiple Web2py applications under the same hostname and the same mod_wsgi site. However, be careful when setting up routes.py or Apache rewrite rules, as these will be shared by the applications.

### Configuration

Sahana Eden is a highly configurable system that can be adapted to many different needs and situations. If you've taken the time planning your project and have answered the questions posed in the "Planning a Deployment" section, you are now simply looking for where to enter the answers.

#### Configuration through the web interface

At the moment only some settings, like SMS, email inbox and Twitter, are editable through the Web UI. Future plans are to add more configuration settings through the Web UI but for now most configuration options require editing text files.

#### Configuration through text files

Many configuration options can be changed by editing models/000_config.py. This consists of sections of Python code where settings for a particular component of the system can be changed. Most of the changes take effect immediately after saving the file. For a production environment then the system would need to be recompiled.
models/000_config.py has to be edited before using Sahana Eden. Once you have edited models/000_config.py, change the FINISHED_EDITING_CONFIG_FILE variable  to True.

There are comments placed next to the options which are generally self-explanatory in nature. Users must not change the variables (or their names), they just need to change their values to configure the instance.

The following sections of models/000_config.py are explained in more detail:

#### Database Settings
It is recommend that production systems use PostgreSQL or MySQL rather than the default SQLite. For these databases it is more secure to provide the application with a database account with minimal privileges.

This section of the models/000_config.py file can be used to configure settings like:

Database Host: The server where your database is hosted
Database Name: The name of the database being used
Username: The username that has been assigned to the user for use with Eden
Password: Password assigned to the user
Port: Port at which the database service is available. Set to None to use the default setting

#### Authentication Settings
Administrators can use these settings to implement security policies and to make sure that there is no unauthorized access or data manipulation in the system. These settings are related to creating the first user account of the system and determining how users register and access the system.

#### Base Settings
Users can configure the system name, the public URL of the system and data pre-population in this section of models/000_config.py.

One of the most important system settings would be the selection of the template as this can completely alter how Sahana operates as well as it's look & feel. A list of available templates is in the folder private/templates. Any template setting can be over-ridden within 000_config.py for further fine-tuning as-required.

One of these settings is database pre-population. Users can determine if the database will be pre-populated with sample data or not.

Changing the database migration setting to False in production will lead to a performance gain. Migration tries to alter the SQL database schema to match that expected in the code. This works very well for simple cases, but may result in loss of existing data for complex cases, so should be applied with care to Production servers.

Web2Py supports automatic migration, but having this enabled all the time does lead to reduced performance, so enable migration only when necessary.

#### Mail Settings
Sahana Eden can be configured to use a email service for messaging. This section can help you to set up things like the outbound email server and sender address. Note: Until the Sender address is specified, the system will be unable to send emails!

#### Front Page Settings
Sahana Eden has a dynamic front page with a capability to display RSS or Twitter feeds. You can change certain aspects of the landing page of the application in the frontpage settings section of the code.

Settings in this section can be used to change which RSS and Twitter feeds are subscribed to and displayed on the front page of the application.

#### Module-specific Settings
Some settings for the Request Management, Inventory Management and Human Resource Management modules can be accessed here. These settings would generally be very specific to the needs of a certain deployment.

#### Enabling/Disabling Modules
Sahana Eden supports a range of modules that can be enabled or disabled to support different deployments. The default template (private/templates/default/) has all the main modules enabled as standard (you may notice that some other modules are disabled as standard; these tend to be under development or experimental).

Disabling a module has the effect of removing it from the main menu of the application. All modules can be disabled except core modules: Home (default), Administration (admin), Map (gis), Person Registry (pr) and Organization Registry (org).

There are three ways to disable modules. The most direct way to do this is to comment out the revelevant lines of code in the configuration file of the default template: private/templates/default/config.py. To turn a line into a comment, simply make sure it begins with a # symbol.
For instance, consider the Shelter Registry (named "cr"). The following code section in private/templates/default/config.py applies to the Shelter Registry:

```python
("cr",
Storage(
    name_nice = T("Shelters"),
    #description = "Tracks the location, capacity and breakdown of victims in Shelters",
    restricted = False,
    module_type = 10,
))
```

To disable this module, just make sure that each line in this section starts with a hash (#) symbol:

```python
#("cr",
#Storage(
#    name_nice = T("Shelters"),
#    #description = "Tracks the location, capacity and breakdown of victims in Shelters",
#    restricted = False,
#    module_type = 10,
#    )),
```

The module is now disabled and will no longer show up in the application menu.

The drawback of this approach, however, is that the default template will be updated whenever you update your code, and any changes you have made risk being lost. For a long-term solution, it is recommended that you create a new template for your implementation.

Most implementations of Sahana Eden involve the creation of a template folder specific for that project. This will be placed within private/templates, as an alternative to the default. The settings.base.template = “default” line within models/000_config.py will then be changed to reflect the name of the new template folder. Eden will initially look within this folder for a config.py file, and if one is present, it will use the module list defined there rather than the one within the default template. To disable unwanted functionality, create a custom version of config.py within your template folder, with unwanted modules commented out as described above.

There is a third option for disabling modules that can be useful in some cases. When testing, for example, or when demonstrating a sub-set of functionality, for example, it may be useful to disable modules without altering the templates. For this, models/000_config.py can be used, and a section of that file is provided for adding in overrides to the template. Add to this section a new line of code for each unwanted module:

```python
settings.modules.pop("unwanted-module-name", None)
``` 
This will remove the module from the list that was created by the template. For example:

```python
settings.modules.pop("cr", None)
```

While the above line is present, the Shelter Registry will be disabled, just like in the previous example. Because updates to the code do not touch models/000_config.py, this change will also be safe from unwanted modification.

For more information on templates, see the Customisation section of this book.

Updates to 000_config.py
So that your configuration settings are not changed when you update the code for your implementation, your local copy of models/000_config.py is not updated with the rest of the code. Very occasionally, however, updates to 000_config.py are necessary. If you do experience problems following an update, it is worth checking your copy of 000_config.py in the models folder with the current version. The current version can be found on your system in private/templates/000_config.py.

Further information on configuring Sahana Eden can also be found at http://eden.sahanafoundation.org/wiki/ConfigurationGuidelines

#### Localization

By default Sahana Eden displays all information in US English. However, the system is fully internationalized, which means that all text elements of the user interface can be displayed in any language, including right-to-left languages.

The process of "localizing" Sahana Eden (adapting it to specific language and locale) involves translating the text elements of the user interface into whatever language is needed.

Many translations are already available for Sahana Eden, although they may not be complete or not up-to-date. These include:

- Arabic
- Bosnian
- Chinese (Simplified)
- Chinese (Traditional)
- Dari
- English (UK)
- French
- German
- Italian
- Japanese
- Khmer
- Korean
- Nepali
- Pashto
- Portuguese (Brazil)
- Portuguese (Portugal)
- Spanish
- Russian
- Tagalog
- Tetum
- Vietnamese
- Malay

#### Updating an Existing Translation
If you need to update an existing translation, either because it is incomplete or to add customized strings specific to your installation, then you need to update a text file in the languages folder (e.g. languages/de.py for the German translation). This file contains a Python dictionary to map the original US English strings to their translated counterparts.

There are 2 approaches that you can take to generate an empty language file for translation:

If you have just a small number of modules that you wish to translate quickly then you can remove all untranslated strings from an existing language file. Then navigate through these modules - this will add any untranslated strings that the system encounters to the language file (assuming the relevant file permissions allow this).
If you wish to translate the entire application as part of a Preparedness project then you can update all the language files in languages by doing the following:

```bash
cd web2py
python web2py.py -S eden -R applications/eden/static/scripts/tools/languages.py
```
There are 3 approaches you can take to do the translations:

Note: Inform all translators to not translate the variables within strings (e.g. %(name)s), but just move around the surrounding text to ensure that the word order makes sense.

1. If you have a small number of strings to translate then it is possible to do this using the Web2Py Admin Interface (this assumes that you have a local branch on your machine to work on):
http://127.0.0.1:8000/admin/default/design/eden#languages

2. If you want to send these strings to be translated by a professional translation company, then they will typically expect the strings in spreadsheet format. You can create a CSV of strings using the Translate Toolkit:

```bash
web2py2po -i language.py -o language.po
po2csv -i language.po -o language.csv
```

Tip: Excel has a nasty habit of corrupting strings with quotation marks or other special characters, so avoid this if possible & be prepared to clean-up if not.

3. If you want to use a community of translators then you can use Pootle (see below).

#### Adding a New Translation
This can be done via the Web2Py admin interface:

http://127.0.0.1:8000/admin/default/design/eden#languages

Create a new file using the ISO 639-1 Code of the Language plus ".py" as the filename. If it is a national variation of a language, eg. New Zealand English, add a suffix to the language code: "en_nz.py".

The same process then applies as for updating an existing language.

#### Using Pootle to Manage Translations
Pootle is a web-based tool to manage translations by a group of translators which includes the ability to have alternate suggestions reviewed before being selected.

There is a Sahana instance at http://pootle.sahanafoundation.org  which is available for you to manage the translation for your language.

To use Pootle you need to convert the .py version of your translation to/from the PO format, which can be done using web2py2po from the Translate Toolkit.

### Maintenance

When Sahana Eden has been deployed, then you need to ensure that the system Availability is maintained through any upgrades and that the Data Integrity isn't compromised by ensuring regular Backups are taken.

#### Backups 

Backups are generally done by dumping the SQL to the filesystem & then copying to tape from there. Also remember to backup the contents of the uploads/ folder

```sql
# Schedule backups for 02:01 daily
echo "1 2   * * * * root    /usr/local/bin/backup" >> "/etc/crontab"
```

#### Scripts

There are a number of useful maintenance scripts which are added to /usr/local/bin by the installation scripts.

(Examples shown are for Apache/MySQL, variants are available for Cherokee and/or PostgreSQL. Check the Installation Guidelines section of the Wiki for the latest versions of these scripts.)

clean
This script is used to reset an instance to default values, which may include 'prepopulated' data specific to this deployment.

```bash

#!/bin/sh
/usr/local/bin/maintenance
cd ~web2py/applications/eden
rm -f databases/*
rm -f errors/*
rm -f sessions/*
rm -f uploads/*
sed -i 's/deployment_settings.base.migrate = False/deployment_settings.base.migrate = True/g' models/000_config.py
sed -i 's/deployment_settings.base.prepopulate = 0/deployment_settings.base.prepopulate = 1/g' models/000_config.py
rm -rf compiled
mysqladmin -f drop sahana
mysqladmin create sahana
cd ~web2py
sudo -H -u web2py python web2py.py -S eden -M -R applications/eden/static/scripts/tools/noop.py
cd ~web2py/applications/eden
sed -i 's/deployment_settings.base.migrate = True/deployment_settings.base.migrate = False/g' models/000_config.py
sed -i 's/deployment_settings.base.prepopulate = 1/deployment_settings.base.prepopulate = 0/g' models/000_config.py
/usr/local/bin/maintenance off
/usr/local/bin/compile

```

w2p
This script is used to open a Python shell in the web2py environment. This allows database migration scripts to be developed interactively.

```bash
#!/bin/sh
cd ~web2py
python web2py.py -S eden -M
```

compile
This script is used to compile the Python code so that changes are visible to users (until this time, chages to .py files aren't seen by users). It is called automatically from the 'pull' and 'clean' scripts.

```bash
#!/bin/sh
cd ~web2py
python web2py.py -S eden -R applications/eden/static/scripts/tools/compile.py
apache2ctl restart
```

maintenance
This script is used to put the site into 'maintenance' mode & restore it to normal operations. It is usually called from the clean & compile  scripts.

```bash
#!/bin/sh
if [ "" != "off" ]
then
    a2dissite maintenance
    a2ensite production
    cd ~web2py && sudo -H -u web2py python web2py.py -K eden -Q >/dev/null 2>&1 &
else
    killall -u web2py python
    a2ensite maintenance
    a2dissite production
fi
apache2ctl restart
```

backup
This does a dump of the SQL database so that it can be backed-up to tape. It is usually called from Cron.

```bash
#!/bin/sh
NOW=$(date +"%Y-%m-%d")
mysqldump sahana > /root/backup-$NOW.sql
OLD=$(date --date='7 day ago' +"%Y-%m-%d")
rm -f /root/backup-$OLD.sql
```

Maintenance Site
This is an alternate Webserver configuration which blocks user access to the application so that upgrades can be done safely. Users see a simple holding page which asks them to try again later. This is (de-)activated by the 'maintenance' script, which is usually called from the 'pull' script.

Tip: It is still possible for administrators to access phpMyAdmin for MySQL database administration whilst the application is offline.

Upgrades
Simple upgrades can be done by running

```bash
git pull upstream
```

If there is a database migration required then this will require extra work. It is highly recommended that Production instances use a Development (and ideally a User Acceptance Testing) instance to practice data migration scripts on. This migration should be done using a copy of the Production database.

When making code customizations, it is best to do this in a branch of the code and then pull that code to the server, rather than editing files directly on the server:

[ServerUpdates](SahanaEden-Git-ServerUpdates_2.png)

Troubleshooting Upgrades
Upgrading the version of Sahana Eden or enabling more modules may require updating configuration settings or installing/upgrading library dependencies.

Update configuration settings file
A new version of Sahana Eden may have new settings in 000_config.py that need to be merged with your current choices. After updating Sahana Eden, compare the copy of 000_config.py in deployment-templates with the site's copy in models. Merge in added and modified lines.
Missing software packages
A new version of Sahana Eden or a newly-enabled module may require software packages that were not included in the original installation. Optional packages may be needed to make use of new features. The latest list of required and optional packages is on the wiki:

http://eden.sahanafoundation.org/wiki/InstallationGuidelines/Windows/Developer/Manual

For optional features that require missing packages, warnings will be printed when the Web2py server is started that list the features and the packages they need. If you don't need this functionality, then these can be safely ignored.

If missing packages are required then attempting to run the application will result in an error ticket with a message saying that this package was not found.

Web2py version
Since Sahana Eden extends Web2Py, and the two are both undergoing rapid development, the revision of Web2Py can be critical. Whilst the latest 'bleeding edge' version of Web2Py is usually stable, some Web2Py revisions have bugs which break a part of Sahana Eden. You can try upgrading to the latest revision of Web2Py or else downgrading to an older version which does not exhibit this bug.

Sometimes a new version of Sahana Eden may use features from a more recent Web2py than the currently installed version.  This typically leads to an error ticket with a message indicating that some item was not found.  Update to either the latest Web2py, or the latest known-stable Web2py revision, the version number for which can be found in private/update_check/eden_update_check.py

It is also sometimes posted in the #sahana-eden IRC channel topic (see the Community chapter for connecting to IRC).