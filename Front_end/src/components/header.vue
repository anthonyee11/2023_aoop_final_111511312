<template>
    <header class="header" id="header">
        <nav class="nav container">
            <a href="#" class="nav__logo">
                <p>Group 6's Final Project</p>
            </a>

            <div class="nav__menu" id="nav-menu">
                <ul class="nav__list">
                   

                  

                    <!-- <a href="#Contact" class="button button--border">Contact Us</a> -->

                </ul>

                <div class="nav__close" id="nav-close">
                    <i class='bx bx-x'></i>
                </div>

            </div>

            <div class="nav__toggle" id="nav-toggle">
                <i class='bx bx-menu'></i>
            </div>

        </nav>
    </header>
</template>


<style>

/*=============== NAV ===============*/

.nav {
    height: var(--header-height);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav__logo {
    display: flex;
    align-items: center;
    column-gap: .5rem;
    font-weight: var(--font-medium);
    padding-left: 5rem;

}

.nav__logo-img {
    width: 1.25rem;
}

.nav__link,
.nav__logo,
.nav__toggle,
.nav__close {
    color: white;
    text-decoration: none;
}

.nav__toggle {
    font-size: 1.25rem;
    cursor: pointer;
}

@media screen and (max-width: 767px) {
    .nav__menu {
        position: fixed;
        width: 100%;
        background: rgb(76, 140, 224);
        top: -150%;
        left: 0;
        padding: 3.5rem 0;
        transition: .4s;
        z-index: var(--z-fixed);
        border-radius: 0 0 1.5rem 1.5rem;
    }
}

.nav__img {
    width: 100px;
    position: absolute;
    top: 0;
    left: 0;
}

.nav__close {
    font-size: 1.8rem;
    position: absolute;
    top: .5rem;
    right: .7rem;
    cursor: pointer;
}

.nav__list {
    display: flex;
    flex-direction: column;
    align-items: center;
    row-gap: 1.5rem;
}

.nav__link {
    text-transform: uppercase;
    font-weight: var(--font-black);
    transition: .4s;
}

.nav__link:hover {
    color: rgb(200, 200, 200);
}


/* Show menu */

.show-menu {
    top: 0;
}


/* Change background header */

.scroll-header {
    background: var(--container-color);
}


/* Active link */

.active-link {
    position: relative;
}

.active-link::before {
    content: '';
    position: absolute;
    bottom: -.75rem;
    left: 45%;
    width: 5px;
    height: 5px;
    background-color: var(--inside-text-color);
    border-radius: 50%;
}
.nav {
        height: calc(3.5rem + 1.5rem);
    }
    .nav__img,
    .nav__close,
    .nav__toggle {
        display: none;
    }
    .nav__list {
        flex-direction: row;
        column-gap: 3rem;
    }
    .nav__link {
        text-transform: initial;
        font-weight: initial;
    }

</style>