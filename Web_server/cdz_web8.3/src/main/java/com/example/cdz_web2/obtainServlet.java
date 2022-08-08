package com.example.cdz_web2;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.annotation.*;
import java.io.IOException;

@WebServlet("/obtainServlet")
public class obtainServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String id=request.getParameter("id");
        String key=request.getParameter("key");
        String MAC=request.getParameter("MAC");
        request.setAttribute("id",id);
        request.setAttribute("key",key);
        request.setAttribute("MAC",MAC);

        response.setHeader( "content-type", "text/html; charset=utf-8");
        response.getWriter().write( "<h1>"+id+",欢迎您!</h1>");
        response.getWriter().write( "<h1>"+key+",欢迎您!</h1>");
        response.getWriter().write( "<h1>"+MAC+",欢迎您!</h1>");

        RequestDispatcher rd=request.getRequestDispatcher("ceshi.html");
        rd.forward(request,response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this.doGet(request, response);
    }
}
