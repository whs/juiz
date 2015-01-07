# Juiz

Juiz is a PaaS-like desktop deployment tool. It can be runs on Linux or OSX.

The development of Juiz is supported by NECTEC under National Software Competition 17 program.

## Features

- Heroku-like environment
- (Mostly) compatible with Heroku buildpack which means language-agnostic
- Supports multiple machine deployment where the database has its dedicated machine, several web backends
- GUI based operation (CLI coming soon)
- Secured firewall settings
- View of remote logs on the GUI
- Execute remote command from the GUI

## Usage

```sh
sudo pip install -r requirements.txt
python main.py gui
```

(You might better install some of the dependencies from your repository.)

Tested on OS X 10.10 and Fedora 21.

## How it works

Juiz use [libcloud](https://libcloud.apache.org/) to perform machines creation. As libcloud is not abstract enough, we wrote several providers to support various cloud provider. The OS of our choice is CentOS 7 as we use systemd quite extensively.

After the machines are created, [Ansible](http://www.ansible.com) is used to perform machine setup. We use Heroku's buildpack to support various languages. As some Heroku buildpack use prebuilt binary that may not be compatible with CentOS 7, some buildpack may need to be modified such as [Python](https://github.com/whs/heroku-buildpack-python).

The GUI part of Juiz is written in wxPython.

## State of the development

Juiz is currently in alpha and is being tested by deploying the backend of [bcbk5](https://github.com/whs/bcbk5/tree/master/bcbk5) to DigitalOcean. This backend however have undergone some modifications to the settings file to allow it to run in Heroku-like environment.

However the Juiz GUI is having a few segfaults on Linux that will be fixed.

There are several additional improvements that under development:

- The EC2 backend is not being tested and t2 instance size is not supported.
- The CloudStack backend is under development
- Currently the API tokens are being stored in the main configuration file. As we plan to make these configuration file checked into VCS the tokens must be stored in a separate, unchecked-in file.
- Managed DNS and load balancer
- CLI deployment

## FAQ

*(wait, who asked these questions? well, presume that you're going to then)*

### Why not do it manually?

The point of PaaS is to simplify the deployment of application. The development doesn't need to know the deployment details and focus on coding instead.

With Juiz you also get the advantage that you can deploy multiple machine which are automatically configured to work together. You only need to code your apps to utilize them.

### Why a PasS doesn't work?

Commercial PaaS is expensive, and open source PaaS needs some setup. Sometimes you only want to install only one application and setting up full PaaS is too much overkill.

Juiz, however does not and will not support multiple tenant where machines are being shared between several applications. If you requires that capability, use a PaaS.

### Why the name Juiz?

[Juiz](http://edenoftheeast.wikia.com/wiki/Juiz) is the name of the concierge AI in Eden of the East series which has 10 billion yen loaded and can be tasked to perform any actions including memory wipe for a price.

My recent projects have the traditional of having anime character names since [Kyou](http://kyou.whs.in.th) (NSC15 winner) which take its name from [Kyou Fujibayashi](http://clannad.wikia.com/wiki/Kyou_Fujibayashi), the kindergarten teacher of an important character.

### License

I don't have a plan for licensing yet, which means that it falls into the latest version of [StealItPL](https://github.com/whs/whs.github.com/blob/master/LICENSE) at this time.

At the end of the NSC program there will be a license announced which may or may not be GNU GPLv3.
