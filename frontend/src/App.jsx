import { Route, Routes } from 'react-router-dom'
import { Provider } from 'react-redux'
import './App.css'
import Client from './pages/client/Client.jsx'
import Home from './pages/Home.jsx'
import NotFound from './pages/NotFound.jsx'
import Contract from './pages/client/Contract.jsx'
import User from './pages/User.jsx'
import AppLayout from './Layout/AppLayout.jsx'
import Roles from './pages/Roles.jsx'
import Permissions from './pages/Permissions.jsx'
import store from './redux/store.jsx'
import Login from './pages/login.jsx'
import SignUp from './pages/SignUp.jsx'
import RequireAuth from './components/RequireAuth.jsx'
import Tickets from './pages/Tickets.jsx'
import TicketDetails from './components/TicketDetails.jsx'
import OAuthCallback from './pages/OAuthCallback.jsx' 

function App() {
  return (
    <Provider store={store}>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path='/' element={<Home />} />
          <Route element={<RequireAuth />}>
            <Route path='/users' element={<User />} />
            <Route path='/client' element={<Client />} />
            <Route path='/client/:client_id/contracts' element={<Contract />} />
            <Route path='/roles' element={<Roles />} />
            <Route path='/permissions' element={<Permissions />} />
            <Route path='/tickets' element={<Tickets />} />
            <Route path='/tickets/:id' element={<TicketDetails />} />
          </Route>
        </Route>

        <Route path='/login' element={<Login />} />
        <Route path='/signup' element={<SignUp />} />
        <Route path='/auth/:provider/callback' element={<OAuthCallback />} />

        <Route path='*' element={<NotFound />} />
      </Routes>
    </Provider>
  )
}

export default App