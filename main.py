import sys

from vulkan import *
from PySide2 import (QtGui, QtCore)

class HelloTriangleApp(QtGui.QWindow):
    def __init__(self):
        super(HelloTriangleApp, self).__init__()

        self.setWidth(1280)
        self.setHeight(720)
        self.setTitle("VK_TEST PySide2")

        self.__instance = None
        self.m_PhysicalDevice = VK_NULL_HANDLE
        self.m_Device = None
        self.m_Surface = None
        
        self.validationLayers =['VK_LAYER_KHRONOS_validation']

        self.initVK()
    def __del__(self):
        if self.__instance:
            vkDestroyInstance(self.__instance, None)
        if self.m_Device:
            vkDestroyDevice(self.m_Device, None)

    def initVK(self):
        self.__createInstance()
        self.pickPhysicalDevice()
        self.checkValidationLayerSupport()
        self.createLogicalDevice()
        self.createSurface()

    def __createInstance(self):
        appInfo = VkApplicationInfo(
            pApplicationName='Python VK',
            applicationVersion=VK_MAKE_VERSION(1, 0, 0),
            pEngineName='No Engine',
            engineVersion=VK_MAKE_VERSION(1, 0, 0),
            apiVersion=VK_API_VERSION
        )
        extensions = [e.extensionName for e in vkEnumerateInstanceExtensionProperties(None)]
        instanceInfo = VkInstanceCreateInfo(
            pApplicationInfo=appInfo,
            enabledLayerCount=0,
            enabledExtensionCount=len(extensions),
            ppEnabledExtensionNames=extensions
        )
        self.__instance = vkCreateInstance(instanceInfo, None)
        
        
    def checkValidationLayerSupport(self):
        # TODO
        layerCount = vkEnumerateInstanceLayerProperties()
        for layer in layerCount:
            print("VL: ", layer)
    
    def pickPhysicalDevice(self):
        devices = vkEnumeratePhysicalDevices(self.__instance)
        assert len(devices) != 0, '[pickPhysicalDevice]: Not found physical devices'
        for device in devices:
            if self.isDeviceSuitable(device):
               self.m_PhysicalDevice = device
                
        assert self.m_PhysicalDevice != VK_NULL_HANDLE, '[pickPhysicalDevice]: Failed to find a suitable GPU'
        
            
    def isDeviceSuitable(self, device):
        deviceProperties = vkGetPhysicalDeviceProperties(device)
        deviceFeatures = vkGetPhysicalDeviceFeatures(device)
        print('GPU: ', deviceProperties.deviceName)
        return deviceProperties.deviceType == VK_PHYSICAL_DEVICE_TYPE_DISCRETE_GPU and deviceFeatures.geometryShader
    
    def createLogicalDevice(self):
        indices = vkGetPhysicalDeviceQueueFamilyProperties(self.m_PhysicalDevice)
        queueFamilyIndex = 0
        qfs = vkGetPhysicalDeviceQueueFamilyProperties(self.m_PhysicalDevice)
        for i, qf in enumerate(qfs):
            if qf.queueCount > 0 and qf.queueFlags & VK_QUEUE_GRAPHICS_BIT:
                queueFamilyIndex = i
                
        queueCreateInfo = VkDeviceQueueCreateInfo(
            sType=VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO,
            queueFamilyIndex=i,
            queueCount=1,
            pQueuePriorities=[1.0]
        )
        deviceFeatures = VkPhysicalDeviceFeatures()
        createInfo = VkDeviceCreateInfo(
            sType=VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO,
            queueCreateInfoCount=0,
            pQueueCreateInfos=queueCreateInfo,
            enabledExtensionCount=0,
            enabledLayerCount=0,
            pEnabledFeatures=deviceFeatures
        )
        
        self.m_Device = vkCreateDevice(self.m_PhysicalDevice, createInfo, None)
        
    def createSurface(self):
        if sys.platform == 'linux':
            from PySide2 import QtX11Extras
            import shiboken2
            connection = QtX11Extras.QX11Info.
            createInfo = VkXcbSurfaceCreateInfoKHR(
                sType=VK_STRUCTURE_TYPE_XCB_SURFACE_CREATE_INFO_KHR,
                window=self.winId(),
            )
        
        
        
        
        

if __name__ == '__main__':
    import sys

    app = QtGui.QGuiApplication(sys.argv)
    win = HelloTriangleApp()
    win.show()
    
    def cleanup():
        global win
        del win
    
    app.aboutToQuit.connect(cleanup)

    sys.exit(app.exec_())
    
    
    
def findQueueFamilies(device):
    res = {'graphicsFamily': None, 'presentFamily': None}
    qfs = vkGetPhysicalDeviceQueueFamilyProperties(device)
    for qf, i in qfs:
        if qf & VK_QUEUE_GRAPHICS_BIT:
            res['graphicsFamily'] = i
            
            

        
