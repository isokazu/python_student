# GIT文档说明
1. git基本命令
> git init 初始化git项目目录  
> 
> git add (文件名) 添加文件到git缓存区
> 
> git commit (文件名) -m "注解" 提交到本地git仓库  
> 
> git checkout -- (文件名) 从仓库恢复文件  
---
2. git工作区
> git stash save "注解" 添加工作区  
> 
> git stash apply (stash@{id}) 取出工作区分支  
> 
> git stash list 查看工作区  
> 
> git stash drop (stash@{id}) 删除一个工作区提交  
> 
> git stash clear 删除工作区所有内容  
---
3. 分支管理
> git branch 查看分支  
> 
> git branch (分支名称) 创建分支  
> 
> git checkout (分支名称) 切换分支  
> ** git checkout -b (分支名称) 创建并切换分支  
> 
> git merge (分支名称) 合并分支  
> 
> git branch -d (分支名称) 删除分支  
> ** git branch -D (分支名称) 强制删除分支  
---
4. 远程仓库使用
> git clone (url) 从远程仓库下载项目到本地文件夹  
> 
> git remote add origin https://github.com/isokazu/python_student.git 在本地git项目中添加远程git主机服务器  
> 
> git remote 查看远程主机  
> 
> 