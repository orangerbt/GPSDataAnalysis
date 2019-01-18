package graphicsEngine;
import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.system.MemoryStack.*;
import static org.lwjgl.system.MemoryUtil.*;
import org.lwjgl.opengl.EXTTextureFilterAnisotropic;
import  org.lwjgl.opengl.GL;
import org.lwjgl.opengl.GL11;
import java.nio.IntBuffer;
import org.lwjgl.glfw.GLFW;
import org.lwjgl.glfw.GLFWCursorPosCallback;
import org.lwjgl.glfw.GLFWErrorCallback;
import org.lwjgl.glfw.GLFWKeyCallback;
import org.lwjgl.glfw.GLFWVidMode;
import org.lwjgl.opengl.GL;
import org.lwjgl.system.MemoryStack;
import engine.KeyboardHandler;
import engine.MouseHandler;

public class Display {
	private long window;
	private int WIDTH;
	private int HEIGHT;
	private int sWIDTH;
	private int sHEIGHT;
	private boolean bool_pause;
	private GLFWKeyCallback keyCallback;
	private GLFWCursorPosCallback mouseCallback;

	public boolean shouldExit;
	
	
	public Display() {
		WIDTH = 900;
		HEIGHT = 900;
		init();
	}
	
	public Display(int width, int height) {
		WIDTH  = width;
		HEIGHT = height;
		sWIDTH = WIDTH;
		sHEIGHT = HEIGHT;
		shouldExit = false;
		bool_pause = false;
		init();
		update();
	}
	
	private void init() {
		
		try {
			
			GLFWErrorCallback.createPrint(System.err).set();
			if ( !glfwInit() ) {
				throw new IllegalStateException("Window error on start");
			}
			glfwDefaultWindowHints(); 
			glfwWindowHint(GLFW_VISIBLE, GLFW_FALSE); 
			glfwWindowHint(GLFW_RESIZABLE, GLFW_TRUE); 
			

			// Create window
			window = glfwCreateWindow(WIDTH, HEIGHT, "0.1.4", NULL, NULL);
			if ( window == NULL )
				throw new RuntimeException("Display failed to launch!!");

			// called each time a key is pressed
			glfwSetKeyCallback(window, (window, key, scancode, action, mods) -> {
				
			});
		} catch(Exception e) {
			 e.printStackTrace();
			    System.out.println("Display Init Failed!");
			    System.exit(0);
		}
		
		GLFWVidMode videoMode = glfwGetVideoMode(glfwGetPrimaryMonitor());
		
		glfwSetWindowPos(window, (videoMode.width()-sWIDTH)/2, videoMode.height()-sHEIGHT/2);
			glfwMakeContextCurrent(window);
			GL.createCapabilities();
			// enable v-sync
			glfwSwapInterval(1);	
			glfwWindowHint(GLFW_SAMPLES, 2);
			GL11.glTexParameterf(GL11.GL_TEXTURE_2D, EXTTextureFilterAnisotropic.GL_TEXTURE_MAX_ANISOTROPY_EXT, 2.0f); 
			glfwShowWindow(window);
			glfwSetKeyCallback(window, keyCallback = new KeyboardHandler());
			glfwSetCursorPosCallback(window, mouseCallback = new MouseHandler());
			glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);


		}



	public void update(){

			// Set color of void rendering
			glClearColor(0.0f, 0.0f, 0.0f, 1.0f);

			// deallocated memory and stops all openGL processes.
			if( glfwWindowShouldClose(window) ) {
				System.exit(0);
			}

			if( ((KeyboardHandler) keyCallback).isKeyDown(GLFW_KEY_ESCAPE)){
				shouldExit = true;
			}

				glfwPollEvents();
				glfwSwapBuffers(window); // swap the color buffers
				
		}
	
	public int getHEIGHT() {
		return HEIGHT;
	}
	public int getWIDTH() {
		return WIDTH;
	}

	public KeyboardHandler getKeyboardHandler() {
		return ((KeyboardHandler)keyCallback);
	}
	public MouseHandler getMouseHandler() {
		return ((MouseHandler)mouseCallback);
	}

	public long getWindowID() {
		return window;
	}
	
	public void pause(boolean bool)
	{
		bool_pause = bool; 
	}

	public void closeDiplay() {
		glfwTerminate();
		System.exit(0);
	}

}
