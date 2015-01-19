" Determine if normal YAML or Ansible YAML
" Language:         YAML (with Ansible)
" Maintainer:       Chase Colman <chase@colman.io>
" Latest Revision:  2013-12-09

autocmd BufNewFile,BufRead *.yml  call s:SelectAnsible()

fun! s:SelectAnsible()
  let fp = expand("<afile>:p")
  let dir = expand("<afile>:p:h")

  " Check if file is called playbook.yml 
  if fp =~ '*playbook.yml'
    set filetype=ansible
    return
  endif

  " Check if buffer is file under any directory of a 'roles' directory
  if fp =~ '/roles/.*\.yml$'
    set filetype=ansible
    return
  endif

  " Check if subdirectories in buffer's directory match Ansible best practices
  if v:version < 704
    let directories=split(glob(fnameescape(dir) . '/{,.}*/', 1), '\n')
  else
    let directories=glob(fnameescape(dir) . '/{,.}*/', 1, 1)
  endif

  call map(directories, 'fnamemodify(v:val, ":h:t")')

  for dir in directories
    if dir =~ '\v^%(group_vars|host_vars|roles)$'
      set filetype=ansible
      return
    endif
  endfor
endfun