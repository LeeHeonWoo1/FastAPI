<script>
  import Router from 'svelte-spa-router'
  import Home from "./routes/Home.svelte"
  import Detail from './routes/Detail.svelte'
  import QuestionCreate from './routes/questions/QuestionCreate.svelte'
  import QuestionModify from './routes/questions/QuestionModify.svelte'
  import AnswerModify from "./routes/answers/AnswerModify.svelte"
  import UserCreate from './routes/users/UserCreate.svelte'
  import UserLogin from './routes/users/UserLogin.svelte'
  import Navigation from './components/Navigation.svelte'

  const routes = {
    '/': Home,
    '/detail/:question_id': Detail,
    '/question-create':QuestionCreate,
    '/user-create':UserCreate,
    '/user-login':UserLogin,
    '/question-modify/:question_id':QuestionModify,
    '/answer-modify/:answer_id': AnswerModify,
  }
</script>

<Navigation />
<Router {routes}/>