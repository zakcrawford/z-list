# symlink to ~/.bash_completion.d/ssh

_ssh_completion()
{
  local cur=${COMP_WORDS[COMP_CWORD]}
  COMPREPLY=( $(compgen -W "echo `cat ~/.ssh/chartboost_hosts | tr '\n' ' '`" -- $cur) )
}

complete -F _ssh_completion ssh
