# IGOS Nusantara's shell defaults (ign-config): the prompt, aliases and ex,
# for interactive bash. ~/.bashrc, read after this, can change any of them.
[ -n "${BASH_VERSION-}" ] && [[ $- == *i* ]] || return 0

# Green for a user, red for root; a line of its own inside tmux.
if [ "$EUID" -eq 0 ]; then
    __ign_user='\[\e[1;31m\]' __ign_mark='#'
else
    __ign_user='\[\e[1;32m\]' __ign_mark='$'
fi
if [ -n "${TMUX-}" ]; then
    PS1="${__ign_user}"'\u\[\e[1;33m\]@\h \[\e[1;35m\]TMUX in \[\e[1;34m\]\w\[\e[0m\] \n'"${__ign_mark} "
else
    PS1="${__ign_user}"'\u\[\e[1;33m\]@\h \[\e[1;35m\]in \[\e[1;34m\]\w\[\e[0m\] '"${__ign_mark} "
fi
unset __ign_user __ign_mark

# Moving around and listing.
alias ..='cd ..'
alias ...='cd ../..'
alias .3='cd ../../../'
alias ll='LC_COLLATE=C ls -lahF --group-directories-first --color=auto --time-style=long-iso'
alias llsort='ll --color=always | sort'
alias llsize='ll --color=always | sort -h -k5'
alias llt='ll -tr'
alias ls='ls --color=auto'
alias grep='grep --color=auto'

# Asking before overwriting or removing.
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# The system and its resources.
alias df='df -h'
alias free='free -m'
alias myip='curl -s https://ifconfig.me && echo'
alias h='history | tail -20'

# Packages.
alias update='sudo dnf update'
alias install='sudo dnf install'
alias search='dnf search'

# Extracts an archive by its extension.
ex() {
    if [ ! -f "$1" ]; then
        echo "'$1' is not a valid file"
        return 1
    fi
    case $1 in
        *.tar.bz2) tar xjf "$1" ;;
        *.tar.gz) tar xzf "$1" ;;
        *.tar.xz) tar xJf "$1" ;;
        *.tar.zst) tar --zstd -xf "$1" ;;
        *.bz2) bunzip2 "$1" ;;
        *.rar) unrar x "$1" ;;
        *.gz) gunzip "$1" ;;
        *.tar) tar xf "$1" ;;
        *.tbz2) tar xjf "$1" ;;
        *.tgz) tar xzf "$1" ;;
        *.zip) unzip "$1" ;;
        *.Z) uncompress "$1" ;;
        *.7z) 7z x "$1" ;;
        *) echo "'$1' cannot be extracted via ex()"; return 1 ;;
    esac
}
