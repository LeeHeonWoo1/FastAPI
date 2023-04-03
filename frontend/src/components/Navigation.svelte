<script>
    import { link } from 'svelte-spa-router'
    import { push } from 'svelte-spa-router'
    // 페이지 정보를 받아오고
    import { page, keyword, access_token, username, is_login } from "../lib/store"
</script>

<!-- 네비게이션바 -->
<nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
    <div class="container-fluid">
        <!-- PYBO로고를 눌렀을 땐 page의 값을 0으로 바꿔 첫 페이지로 이동할 수 있게끔 변수를 0으로 만들어준다. -->
        <a use:link class="navbar-brand" href="/" on:click="{() => {$keyword = '', $page = 0}}">Dancey</a>
        <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation">
            <span class="navbar-toggler-icon" />
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                {#if $is_login }
                    <li class="nav-item">
                        <a use:link href="/user-login" class="nav-link" on:click={() => {
                            $access_token = ''
                            $username = ''
                            $is_login = false
                            push('/')
                        }}>로그아웃 ({$username})</a>
                    </li>
                {:else}
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/user-create">회원가입</a>
                    </li>
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/user-login">로그인</a>
                    </li>
                {/if}
            </ul>
        </div>
    </div>
</nav>