# grapy

## About
Grapy 🍇 is a tool to program workflows by defining them as graphs.
Thanks to modularity you can customize how these graph workflows are executed and how they are represented.
Thanks to graphical representation you can see it at requested degree of complexity - whether you want to focus on details of specific part or take a wider look at the whole.
Thanks to composite, intuitive user interface it makes composing workflows easier and forgiving.

### Why?  
To be able to create workflows using graphs. What should ensure that the coded workflow is more readable, easier to influence its course (e.g., adding monitoring, logging), and can be visualized. Graphs are used to give a specific structure to workflows. Additionally, they allow for creating very complex workflows.

### Aim  
In other words, the desired effect, the place where we want to be.
We have a user-friendly tool that allows us to create and easily manage complex processes. It enables us to see the whole picture, but in a way that the human brain can grasp at a glance.

### Suggestions  
- using only built-in libraries - it will be difficult with the graph. As a workflow processor, it would probably be possible
- removing elements such as the way of processing the workflow graph, the engine controlling the graph (e.g. the Networx package) - the possibility of expansion and reducing dependencies on external libraries
- node = pipeline ; edge = syntactic mapping / transfer route - this “syntactic mapping” will not be very clean, legible, and secondly, it does not work well with the concept of a graph. Although it may seem logical (in the step-by-step convention where node = step)
- node = state / map / space ; edge = pipeline - it may not seem logical at first glance, but this is what will give a clear picture, both for returning and for creating (in the milestone-transformation-milestone convention; node = milestone, edge = transformation, or as a stock-flow systemic approach)
- NEW levels! The point is that edges themselves can be graphs (workflow graph). In this way, you can easily control the levels of abstraction and, above all, grasp the whole thing at one glance. And if something interests you then you can expand it and dig around.
- NEW visualization seems to be necessary if we want to have benefits from this approach. Not GUI but the ability to look at the structure yes. And if it is additionally interactive (meaning that you can click on a connection/edge and see the details)
- NEW uniform interface, like Lego blocks. That is, all blocks have the same connectors/sockets



### API drafts
```
wg = WorkflowGraph(protocol=protocols.name, engine=graph_engines.networkx_engine)
wg.print
data_node = wg.add_node(‘data’)
edge1 = wg.add_edge(‘start’,’data’)
edge1.append(data.downloaders.yf)

wg[‘start’][‘store’] = data params
result = wg() # saved also in data_node[‘store’]
#OR 
result = wg(data params)

feats_node = wg.add_node(‘feats’)
edge2 = wg.add_edge(data_node, feats_node)
edge2.append(transform_func) 
```

## Environment

### Supported Python versions

Tested via GitLab pipeline against 3.9 - 3.12. Base version is 3.10.

### Development environment

Conda is used for local development, only to keep specific Python version. 
- environment.yml - this is common conda environment specification.
- conda-spec-file.txt - this is explicit specification. Use command from the heading of this file to create development environment.

Activate with `conda activate grapy_env`

**This will not be updated unless Python version is to be changed**

### Working environment

*(First have your conda env activated or python with correct version available)*
Traditionall `venv` is used here. `requirements.txt` will be updated as needed (`pip freeze > requirements.txt`.
To activate on windows run `venv/Scripts/active.bat`.

-----------------
*gitlab template:*

## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.com/codingtools/grapy.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab.com/codingtools/grapy/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
